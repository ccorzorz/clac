#!/usr/bin/env python
# -*-coding=utf-8-*-
# Auther:ccorz Mail:ccniubi@163.com Blog:http://www.cnblogs.com/ccorz/
# GitHub:https://github.com/ccorzorz

import re,os

#提高计算效率,使用re.compile写入正则匹配,提前编译
#匹配外部有内部没有小括号的部分
bracket_flag_str=re.compile('(\([^()]+\))')
#从左到右匹配乘除部分
mul_div_exec_str=re.compile('\d+\.*\d*[\*\/]+[\+\-]?\d+\.*\d*')

def sign_exec(args):
    """
    加减处理,将+-替换为-,--替换为+
    :param args: 表达式字符串
    :return: 将替换后的结果返回
    """
    return re.sub(r'\+\-','-',re.sub(r'\-{2}','+',args))


def add_sub_exec(args):
    """
    加减计算功能
    :param args: 字符串
    :return: 求和的结果
    """
    if args.startswith('-'):    #如果以-开头,将开头的加一个0
        args='0%s'%(args)
    elif args.startswith('+'):  #如果以+开头,将开头的+去掉
        args=re.sub(r'\+','',args)
    args=re.sub(r'\-','+-',args)    #将所有的-替换为+-
    args_list=re.split(r'\+',args)  #以+将字符串分割为列表
    for i in args_list:
        args_list[args_list.index(i)]=float(i)  #列表中的元素转化为float类型
    result=sum(args_list)   #求和
    return result


def exec_had_drop_contect(args):
    """
    处理括号内优先计算的函数
    :param args: 字符串
    :return: 递归函数
    """
    if not mul_div_exec_str.search(args): #如果不匹配,说明已经计算完成
        return args
    else:
        #以优先计算的部分,将字符串分割成两部分
        before,after=mul_div_exec_str.split(args,1)
        #优先计算部分定义变量
        contect=mul_div_exec_str.search(args).group()
        #如果以*分割后的列表长度大于1,计算值
        if len(contect.split('*'))>1:
            v1,v3=contect.split('*')
            v=float(v1)*float(v3)
        else:
            #处理除法
            v1,v3=contect.split('/')
            #如果除以0,提示并退出程序
            if float(v3)==float(0):
                exit('\033[31;1m学渣!!!!学渣!!!!学渣!!!!能'
                     '特么除以0么?体育老师教的数学??!!\033[0m')
            else:
                #处理除法结果
                v=float(v1)/float(v3)
        #拼接字符串
        new_str='%s%s%s'%(before,v,after)
        #拼接后的字符串进行加减号处理
        had_sign_exec_str=sign_exec(new_str)
        #args重新赋值
        args=had_sign_exec_str
    return exec_had_drop_contect(args)


def drop_brakets(args):
    """
    括号处理函数
    :param args: 字符串表达式
    :return: 递归函数
    """
    #如果不匹配说明已经没有括号,结束递归
    if not bracket_flag_str.search(args):
        return args
    else:
        #匹配优先的计算的内容,并且风格为3部分
        before,mid,after=bracket_flag_str.split(args,1)
        #打印分割部分,提示用户计算进度
        print(before,mid,after)
        #字符串去掉括号
        had_drop_contect=mid[1:-1]
        #计算优先部分,先计算乘除,再将结果进行加减运算
        add_sub_result=exec_had_drop_contect(had_drop_contect)
        result=add_sub_exec(add_sub_result)
        #将结果返回原来的字符串,拼接为新字符串
        args='%s%s%s'%(before,str(result),after)
    return drop_brakets(args)


def calc(args):
    """
    计算数据函数,先处理括号部分,然后计算乘除,最后加减部分,返回结果
    :param args: 字符串
    :return: 计算结果
    """
    no_brakets=drop_brakets(args)
    no_mul_div=exec_had_drop_contect(no_brakets)
    result=add_sub_exec(no_mul_div)
    print('\033[31;1m%s\033[0m'%result)

def check_formula(args):
    """
    判断用户输入字符串的可用性,检查括号数量是否匹配
    :param args:   #字符串
    :return:
    """
    if len(re.findall('\(',args)) == len(re.findall('\)',args)):
        return True
    else:
        #不匹配无法运行
        print('括号数量不匹配,确认后再输入')
        return  False

#运行主函数
if __name__ == '__main__':
    #清屏
    os.system('clear')
    print('欢迎使用只带小括号计算器'.center(60,'*'))
    inp=input('请输入你要算的表达式,除了加减乘除小括号,其他都不支持哦:')
    #先将输入的字符串去掉空白部分,以免报错
    inp=inp.strip()
    res=check_formula(inp)
    if res:
        #如果字符串符合表达式格式,进行计算
        calc(inp)
    else:
        #否则退出
        exit('输入格式有误')
