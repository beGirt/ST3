|  Category  |   Value    |
| :--------: | :--------: |
|    学号    | 1840611623 |
|    姓名    |   林盛锋   |
| 数据库软件 |   MySQL    |

> 目录
>
> >[DDL](#1)
> >
> >[DML](#2)
> >
> >[视图](#3)

- <span id = "1">DDL部分</span>

``` mssql

-- 创建数据库
CREATE DATABASE BookManager;
-- 创建student表
CREATE TABLE student(
	sno VARCHAR(10) NOT NULL COMMENT '学号',
    sname VARCHAR(10) COMMENT '学生姓名',
    ssex CHAR(10) COMMENT '性别',
    sbirth DATE COMMENT '出生日期',
    sdept VARCHAR(10) COMMENT '所属系名称',
    PRIMARY KEY (sno)
) COMMENT '学生表';
-- 创建book表
CREATE TABLE book(
	bno VARCHAR(10) not null COMMENT '书号',
    bname VARCHAR(255) COMMENT '书名',
    author CHAR(32) COMMENT '作者',
    price float COMMENT '价格',
    publish VARCHAR(255) COMMENT '出版社',
    book_number smaillint(6) COMMENT '库存量',
    PRIMARY KEY (bno)
) COMMENT '书籍表';
-- 创建borrowstore表
CREATE TABLE borrowstore(
	sno VARCHAR(10) NOT NULL COMMENT '学号',
    bno VARCHAR(10) NOT NULL COMMENT '书号',
    borrowdate DATE COMMENT '借书日期',
    restoredate DATE COMMENT '还书日期',
    latedate DATE COMMENT '还书期限',
    fine float COMMENT '罚金',
    PRIMARY KEY (sno,bno)
) COMMENT '借还关系表';


-- UPDATE DELETE INSERT 实训
-- 1)李小同 从中文系转到计算机系
UPDATE student SET 
	sdept = '计算机系' 
WHERE
	sname = '李小同' 
	AND sdept = '中文系'
-- 2)图书馆今天为《数据库原理》进了5本书
UPDATE book SET
	book_number = book_number + 5
WHERE
	bname = '数据库原理'
-- 3）图书馆不再存放《大学英语》这种书
DELETE FROM book
WHERE 
	bname = '大学英语'
-- 4）王强于 2020-02-25 借了一本《数据库原理》
INSERT INTO borrowstore(sno,bno,borrowdate) VALUES(
	(SELECT sno FROM student WHERE sname = '王强'),
    (SELECT bno FROM book WHERE bname = '数据库原理'),
    '2020-02-25'
)
-- 5）为借还书表增加一个罚款字段fine 类型是float，用于记录逾期未还时需要缴纳的费用
ALTER TABLE borrowstore ADD COLUMN fine float
-- 6）王强于2020-03-28将《数据库原理》归还
UPDATE borrowstore SET
	restoredate = '2020-03-28'
WHERE
	sno = (
    	SELECT sno
        FROM
        	student
        WHERE
        	sname = '王强'
    )
	
	
```





---

>关于导入数据:
>
>1. 将Excel文件转为csv为后缀的文件
>
>2. 再用图形化界面导入(例如phpMyAdmin,DBeaver,MySQL-Workbench)

---



- <span id = "2">DML实训部分（单表查询）</span>
``` mysql
-- 1) 统计图书馆共有多少种图书
SELECT 
	COUNT(*) 
FROM 
	book

-- 2)按年龄从大到小列出所有女同学的学号 姓名 性别 和 年龄
SELECT
	Sno,Sname,Ssex,Sage 
FROM
	Student s 
WHERE 
	s.Ssex = '女'
ORDER BY 
	Sage DESC 

-- 3)查询1001同学的借书总量
SELECT 
	COUNT(*) 
FROM
	borrowstore b2 
WHERE 
	b2.sno = '1001'

-- 4)查询清华大学出版社带有 数据库 三字的图书信息,包括书号,书名
SELECT
	bno,bname 
FROM
	book b 
WHERE 
	b.publish = '清华大学出版社'
and 
	b.bname like '%数据库%'

-- 5)查找2019年平均罚款金额
SELECT 
	AVG(bs.fine) 
FROM 
	borrowstore bs 
WHERE 
	DATE_FORMAT(bs.borrowdate, '%Y') = '2019'
-- 6)查询今年共有多少学生借书
SELECT 
	COUNT(DISTINCT bs.sno) 
FROM 
	borrowstore bs 
WHERE 
	DATE_FORMAT(bs.borrowdate, '%Y') = '2020'		

-- 7)查询今年三月的所有借书信息,并且按借书量降序排序
SELECT 
    bs.bno, 
    COUNT(*) 
FROM 
	borrowstore bs 
WHERE 
	DATE_FORMAT(bs.borrowdate, '%Y-%m-%d') BETWEEN '2020-03-01' 
	AND '2020-03-31' 
GROUP BY 
    bs.bno 
    ORDER BY 
    COUNT(*) DESC

-- 8)查询b01图书不在2018-2019年期间的借书记录
SELECT 
	* 
FROM 
	borrowstore b1 
WHERE 
    bno = 'b01' 
    AND DATE_FORMAT(borrowdate, '%Y') NOT BETWEEN '2018' 
    AND '2019' 

-- 9)查询清华大学 and 人命邮电和高等教育3家出版社的所有图书号 书名 出版社 和 库存量升序排列
SELECT 
	b.bno,b.bname,b.publish,b.book_number
FROM 
	book b 
WHERE 
    b.publish in (
    '清华大学出版社', '高等教育出版社', 
    '人民邮电出版社'
    ) 
ORDER BY 
	b.book_number DESC 

-- 10)查询图书库存总量低于10本的出版社名.
SELECT 
	publish, 
	SUM(book_number) 
FROM 
	book b 
GROUP BY 
	publish 
HAVING 
	sum(book_number) < 10 
```





- ### DML实训部分 (多表查询)


``` mysql
-- 1)查询所有学生的借书情况,包括学生姓名 图书名 借书日期
SELECT 
	s.sname, 
	b.bname, 
	bs.borrowdate 
FROM 
	student s, 
	book b, 
	borrowstore bs 
WHERE 
	s.sno = bs.sno 
	AND b.bno = bs.bno
-- 2)查询借阅了清华大学出版社且书名包含"数据库"三个字的读者 显示姓名 书名 出版社 借书日期 还书日期
SELECT 
	s.sname, 
	b.bname, 
	b.publish, 
	bs.borrowdate, 
	bs.restoredate 
FROM 
	student s, 
	book b, 
	borrowstore bs 
WHERE 
	s.sno = bs.sno 
	AND b.bno = bs.bno 
	AND b.publish = '清华大学出版社' 
	AND b.bname LIKE '%数据库%'
-- 3)按学生最喜欢的书列出图书排行榜,包括书号 书名 出版社
SELECT 
	b.bno, 
	b.bname, 
	COUNT(DISTINCT bs.sno) 
FROM 
	book b, 
	borrowstore bs 
WHERE 
	b.bno = bs.bno 
GROUP BY 
	b.bno 
ORDER BY 
	COUNT(*)
-- 4)查询至少借阅过1本清华大学出版社的读者 显示学号 姓名 书本名称 借阅日期 并且按借阅本身降序排序
SELECT 
	s.sno, 
	s.sname, 
	b.bname, 
	bs.borrowdate 
FROM 
	student s, 
	book b, 
	borrowstore bs 
WHERE 
	s.sno = bs.sno 
	AND b.bno = bs.bno 
	AND b.publish = '清华大学出版社' 
ORDER BY 
	bs.borrowdate
-- 5)查询逾期未还的读者 显示姓名 书名
SELECT 
	s.sname, 
	b.bname
-- 	bs.borrowdate, 
-- 	bs.restoredate, 
-- 	bs.latedate 
FROM 
	student s, 
	book b, 
	borrowstore bs 
WHERE 
	s.sno = bs.sno 
	AND b.bno = bs.bno 
	AND (bs.restoredate > bs.latedate) 
	OR (
		bs.restoredate = NULL 
		AND bs.latedate < CURRENT_DATE
	)
-- 6)按学号统计每个学生的姓名和借书总量
SELECT 
	s.sname, 
	COUNT(*) 
FROM 
	student s, 
	borrowstore bs 
WHERE 
	s.sno = bs.sno 
GROUP BY 
	s.sno
-- 7)统计从未借过书的学生学号和姓名
SELECT 
	s.sno, 
	s.sname 
FROM 
	student s 
WHERE 
	s.sno NOT IN (
		SELECT 
			bs.sno 
		FROM 
			borrowstore bs
	)
-- 8)查询从未被借阅过的图书号和图书名
SELECT 
	b.bno, 
	b.bname 
FROM 
	book b 
WHERE 
	b.bno NOT IN (
		SELECT 
			bs.bno 
		FROM 
			borrowstore bs
	)
```



- DML实训部分（嵌套、集合查询）

```mysql

-- 1）查询与《数据库原理》同价位的信息，并按库存量降序排列
SELECT 
	* bna
FROM
	book b1
WHERE
	b1.price = (
    	SELECT 
        	b2.price
        FROM
        	book b2
       	WHERE
        	b2.bname = '数据库原理'
    )
ORDER BY
	b1.book_number
-- 2)查询价格超过图书馆平均价格的图书编号、名称、出版社、价格
SELECT 
	b1.bno,
	b1.bname,
	b1.publish,
	b1.price
FROM 
	book b1
WHERE
	b1.price > (
    	SELECT 
        	AVG(b2.price)
        FROM
        	book b2
    )
-- 3)查询同时借阅了《数据库原理》和《C语言程序设计》的学生的学号和姓名
-- 方法一
SELECT 
	* 
FROM 
	student s 
WHERE 
	s.sno in (
		SELECT 
			bs1.sno 
		FROM 
			borrowstore bs1 NATURAL 
			JOIN book b1 
		WHERE 
			b1.bname = '数据库原理' 
			AND bs1.sno IN (
				SELECT 
					bs2.sno 
				FROM 
					borrowstore bs2 NATURAL 
					JOIN book b2 
				WHERE 
					b2.bname = 'C语言程序设计' 
					AND bs1.borrowdate = bs2.borrowdate
			)
	)
-- 方法二
SELECT 
	* 
FROM 
	student 
WHERE 
	sno IN (
		SELECT 
			bs2.sno 
		FROM 
			borrowstore bs1, 
			borrowstore bs2 
		WHERE 
			bs1.bno = (
				SELECT 
					b1.bno 
				FROM 
					book b1 
				WHERE 
					b1.bname = '数据库原理'
			) 
			AND bs2.bno = (
				SELECT 
					b2.bno 
				FROM 
					book b2 
				WHERE 
					b2.bname = 'C语言程序设计'
			) 
			AND bs1.borrowdate = bs2.borrowdate
	)
-- 查询与‘王强’在同一天借书的读者的学号、姓名、系别
-- 只要一天就行
SELECT
	s1.sno,
	s1.sname,
	s1.sdept
FROM
	student s1
WHERE
	EXISTS(
    	SELECT
        	*
        FROM
        	borrowstore bs1
        WHERE
        	bs1.borrowdate in (
            	SELECT 
                	bs2.borrowdate
                FROM
                	borrowstore bs2
            	WHERE
                	bs2.sno = (
                    	SELECT
                        	s2.sno
                        FROM 
                        	student s2
                        WHERE
                        	s2.sname = '王强'
                    )
            )
    )
-- 完全重合
-- 没有一天 王强去借书 该同学没去借书
SELECT 
	s2.sno, 
	s2.sname, 
	s2.sdept 
FROM 
	student s2 
WHERE 
	NOT EXISTS (
		SELECT 
			*
        FROM 
			borrowstore bs1
        WHERE 
			NOT EXISTS (
            	SELECT 
                	*
                FROM 
                	borrowstore bs2
                WHERE
                	bs2.sno = (
                    	SELECT
                    		s2.sno
                        FROM
                        	student s2
                        WHERE
                        	s2.sname = '王强'
                    ) 
                	AND bs2.borrowdate = bs1.borrowdate
            )
    )
-- 统计去年借书频率低于2的系 

-- 方法1：视图法
CREATE VIEW dept AS (
	SELECT
    	sdept
    FROM
    	student
)

CREATE VIEW borrowstore_dept AS (
	SELECT 
    	s1.sdept,bs1.sno,bs1.bno,bs1.borrowdate,bs1.restoredate
    FROM
    	student s1,
    	borrowdate bs1
    WHERE
    	s1.sno = bs1.sno
)

SELECT 
	d1.sdept
FROM
	dept d1
WHERE
	2 > (
    	SELECT 
        	COUNT(*)
        FROM
        	borrowstore_dept bsd1
        WHERE
        	d1.sdept = bsd1.sdept
        	AND DATE_FORMAT(bsd1.borrowdate,'%Y') = '2019' 
    )
-- 查询和‘王强’还书总数相同的读者的学号和姓名
SELECT 
	s1.sno, 
	s1.sname 
FROM 
	student s1 
	INNER JOIN borrowstore bs1 ON s1.sno = bs1.sno 
WHERE 
	bs1.restoredate IS NOT NULL 
GROUP BY 
	s1.sno 
HAVING 
	COUNT(*) = (
		SELECT 
			COUNT(*) 
		FROM 
			borrowstore bs2 
		WHERE 
			bs2.sno = (
				SELECT 
					s2.sno 
				FROM 
					student s2 
				WHERE 
					s2.sname = '王强'
			) 
			AND bs2.restoredate IS NOT NULL
	)
-- 查询借阅了清华大学出版社但是没有借阅人们邮电出版社的学生的学号和姓名
SELECT 
	s1.sno, 
	s1.sname 
FROM 
	student s1 
WHERE 
	s1.sno IN (
		SELECT 
			bs1.sno 
		FROM 
			borrowstore bs1, 
			book b1 
		WHERE 
			bs1.bno = b1.bno 
			AND b1.publish = '清华大学出版社' 
			AND bs1.sno NOT IN (
				SELECT 
					bs2.sno 
				FROM 
					borrowstore bs2, 
					book b2 
				WHERE 
					b2.bno = bs2.bno 
					AND b2.publish = '人民邮电出版社'
			)
	)
-- 查询2020年3月以后没有借书的学生的学号、姓名、系别
SELECT 
	s1.sno,
    s1.sname
FROM 
	student s1 
	LEFT OUTER JOIN borrowstore bs1 ON s1.sno = bs1.sno 
	AND DATE_FORMAT(bs1.borrowdate, '%Y-%m') > '2020-03' 
WHERE 
	bs1.sno IS NULL
-- 查询正在借阅的图书的书号、书名和出版社
SELECT 
	b1.bno,
	b1.bname,
	b1.publish
FROM
	book b1 
	LEFT OUTER JOIN borrowstore bs1 ON b1.bno = bs1.bno
WHERE
	bs1.borrowdate IS NOT NULL 
	AND bs1.restoredate IS NULL
-- 查询图书全部还清的系，并显示该系的所有借书记录
SELECT 
	*
FROM 
	student s1,
	borrowstore bs2
WHERE
	s1.sno = bs2.sno
    AND NOT EXISTS(    
        SELECT
            *
        FROM
            borrowstore bs1
        WHERE
            s1.sno = bs1.sno
            AND bs1.restoredate IS NULL
        GROUP BY 
        s1.sdept
    )
ORDER BY
	s1.sdept
                                                                               
                                                                               
                                                                               
```





- <span id = "3">视图相关</span>

``` mysql
-- SQL之视图相关

-- 1）为清华大学出版社的图书创建一个视图
CREATE VIEW QH_Book AS (
	SELECT
    	*
    FROM 
    	book
    WHERE
    	publish = '清华大学出版社'
)
-- 2）通过 1）视图完成查询清华大学出版社所有图书的信息
SELECT 
	* 
FROM 
	QH_Book
-- 3）通过 1）视图完成查询清华出版社价格在50元以上的图书信息
SELECT 
	* 
FROM 
	QH_Book qb 
WHERE 
	qb.price > 50
-- 4）通过 1）视图更新“数据库原理”这本书的作者是‘李言松’
UPDATE 
	QH_Book qb 
SET 
	qb.author = '李言松' 
WHERE 
	qb.bname = '数据库原理'

```

