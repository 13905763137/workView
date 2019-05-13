import pymysql
import pandas as pd

connect = pymysql.Connect(
    host='ip',
    port=3306,
    user='root',
    passwd='pass',
    db='dbname',
    # charset='utf8'
)

# 获取游标
cursor = connect.cursor()


def get_all_data():
    # 查询数据
    sql = "SELECT * FROM work"
    cursor.execute(sql)
    data = pd.DataFrame(list(cursor.fetchall()))
    return data


data = get_all_data()
# 选择需要显示的字段
data = data[[2, 7, 4, 5, 9]]
# 打印输出
data1 = list(data[4])
data2 = list(data[9])
count_undergraduate = 0
master = 0
doctor = 0
others = 0
college = 0
unlimited = 0
unrestricted = 0
graduate = 0
one_year = 0
almost_year = 0
three_year = 0
five_year = 0
for data1 in data1:
    if data1 == "本科":
        count_undergraduate = count_undergraduate + 1
    elif data1 == "硕士":
        master = master + 1
    elif data1 == "博士":
        doctor = doctor + 1
    elif data1 == "大专":
        college = college + 1
    elif data1 == "不限":
        unlimited = unlimited + 1
    else:
        pass
for data2 in data2:
    if data2 == "应届毕业生" or data2 == "应届" or data2 == "应届生":
        graduate = graduate + 1
    elif data2 == "不限":
        unrestricted = unrestricted + 1
    elif data2 == "1年" or data2 == "2年" or data2 == "1-3年":
        one_year = one_year + 1
    elif data2 == "3年" or data2 == "4年" or data2 == "3-5年":
        three_year = three_year + 1
    elif data2 == "5年" or data2 == "6年" or data2 == "5-7年":
        five_year = five_year + 1
    elif data2 == "一年以下":
        almost_year = almost_year + 1
    else:
        pass


def get_data(job_name):
    sql = "SELECT * FROM work where jobName like '%{0}%'".format(job_name)
    cursor.execute(sql)
    return cursor.fetchall()


def get_cloud():
    sql = "SELECT jobName,COUNT(1) from `work` GROUP BY jobName;"
    cursor.execute(sql)
    return cursor.fetchall()


def get_areacity():
    sql = "SELECT city,COUNT(1) as totel from `work` GROUP BY city ORDER BY totel desc LIMIT 10;"
    cursor.execute(sql)
    return cursor.fetchall()


def get_salary():
    data_pd = get_all_data()
    dom = data_pd[[4, 5]]
    data = [[], [], [], [], []]
    dom1, dom2, dom3, dom4, dom5 = data
    for i, j in zip(dom[4], dom[5]):
        try:
            if 'K' in j and '以下' not in j:
                j = ((float(j.split('-')[0].replace('K', '')) + float(j.split('-')[1].replace('K', ''))) / 2) * 1000
            elif '薪资面议' in j:
                continue
            elif 'K' not in j:
                j = ((float(j.split('-')[0]) + float(j.split('-')[1])) / 2)
            elif '以下' in j:
                j = (float(j.split('-')[0].replace('K', ''))) * 1000
            else:
                continue
        except Exception as e:
            continue
        if '大专' in i:
            dom2.append(j)
        elif '本科' in i:
            dom3.append(j)
        elif '博士' in i:
            dom4.append(j)
        elif '硕士' in i:
            dom5.append(j)
        else:
            dom1.append(j)

    salary1_count = ['3k以下', compare_salay(dom2)[0], compare_salay(dom3)[0], compare_salay(dom5)[0],
                    compare_salay(dom4)[0]]
    salary2_count = ['3k-7k', compare_salay(dom2)[1], compare_salay(dom3)[1], compare_salay(dom5)[1],
                     compare_salay(dom4)[1]]
    salary3_count = ['7k-11k', compare_salay(dom2)[2], compare_salay(dom3)[2], compare_salay(dom5)[2],
                     compare_salay(dom4)[2]]
    salary4_count = ['11k-15k', compare_salay(dom2)[3], compare_salay(dom3)[3], compare_salay(dom5)[3],
                     compare_salay(dom4)[3]]
    salary5_count = ['15k以上', compare_salay(dom2)[4], compare_salay(dom3)[4], compare_salay(dom5)[4],
                     compare_salay(dom4)[4]]
    return (salary1_count, salary2_count, salary3_count, salary4_count, salary5_count)


def compare_salay(salary):
    salary1_num, salary2_num, salary3_num, salary4_num, salary5_num = 0, 0, 0, 0, 0
    for i in salary:
        if i < 3000 and i > 0:
            salary1_num += 1
        elif i >= 3000 and i < 7000:
            salary2_num += 1
        elif i >= 7000 and i < 11000:
            salary3_num += 1
        elif i >= 11000 and i < 15000:
            salary4_num += 1
        else:
            salary5_num += 1
    return [salary1_num, salary2_num, salary3_num, salary4_num, salary5_num]
