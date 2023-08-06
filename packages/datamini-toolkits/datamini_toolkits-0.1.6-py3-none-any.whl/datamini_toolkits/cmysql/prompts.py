_RELATIONS_FORMAT="""
# 实体：表
t_order
t_user

# 实体：字段
t_order.id
t_order.user_id
t_user.id

# 表之间的关系：表1->表2 表示表1中的某个字段与表2的主键关联
t_order->t_user

# 字段与表的归属关系
t_order.id->t_order
t_order.user_id->t_order
t_user.id->t_user

# 字段和字段之间的关系，字段1->字段2 表示字段1与字段2关联，且字段2是主键
t_order.user_id->t_user.id
"""


META_TO_RELATIONS="""

在一个关系型数据库中，表和表之间是有一些关联关系，比如两个表有相同含义的字段，存储的是同一个数据，可用于JOIN，那这两个表就是有关联关系的。

请根据如下给出的建表语句，找出他们的关系，并按格式返回。

{SHOW_CREATE_TABLE_SQL}

返回的格式如下：
""" + _RELATIONS_FORMAT




RELATIONS_TO_GQL="""

请根据如下的实体和关系信息，生成一个Neo4j图数据库的数据导入语句。
要求
1，生成的语句可以导入到Neo4j中
2，只有两类实体，表和字段，表的属性有表名，字段的属性有字段名
3，有3类关系：表之间的关系，字段与表的归属关系，字段和字段之间的关系

关系信息如下：
{RELATIONS_INFO}
"""

