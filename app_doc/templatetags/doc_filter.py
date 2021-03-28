# coding:utf-8
# 手册自定义模板过滤器
from app_doc.models import *
from django import template
import re

register = template.Library()

# 获取手册的子手册
@register.filter(name='get_next_doc')
def get_next_doc(value):
    data = Doc.objects.filter(parent_doc=value,status=1).values('id','name').order_by('sort')
    return data

# 获取手册的所属文集
@register.filter(name='get_doc_top')
def get_doc_top(value):
    try:
        return Project.objects.get(id=int(value))
    except Exception:
        return ''

# 获取用户是否为文集创建者
@register.filter(name='is_colla_pro')
def is_colla_pro(pro,user):
    p = Project.objects.filter(id=pro,create_user=user)
    if p.exists():
        return ''
    else:
        return '【协作】'

# 获取手册的上级手册名称
@register.filter(name='get_doc_parent')
def get_doc_parent(value):
    if int(value) != 0:
        return Doc.objects.get(id=int(value))
    else:
        return '无上级手册'

# 获取手册的下一篇手册
@register.filter(name='get_doc_next')
def get_doc_next(value):
    try:
        doc_id = value
        doc = Doc.objects.get(id=int(doc_id))  # 当前手册
        docs = Doc.objects.filter(
            parent_doc=doc.parent_doc,
            top_doc=doc.top_doc,
            status=1
        ).order_by('sort')  # 同级所有手册
        docs_list = [d.id for d in docs]

        subdoc = Doc.objects.filter(parent_doc=doc.id,top_doc=doc.top_doc, status=1)  # 获取当前手册的所有子级手册

        # 没有下级手册
        if subdoc.count() == 0:
            # 如果手册为同级最后一个手册，则没有下一篇手册
            if docs_list.index(doc.id) == len(docs_list) - 1:
                try:
                    parentdoc = Doc.objects.get(id=doc.parent_doc)  # 获取当前手册的上级手册
                    parents = Doc.objects.filter(parent_doc=parentdoc.parent_doc, top_doc=doc.top_doc, status=1).order_by('sort')  # 获取上级手册的所有同级手册
                    parent_list = [d.id for d in parents]
                except:
                    return None
                if parent_list.index(parentdoc.id) == len(parent_list) - 1:
                    # 获取上级手册的上一级手册
                    try:
                        parentdoc2 = Doc.objects.get(id=parentdoc.parent_doc)
                        parents2 = Doc.objects.filter(parent_doc = parentdoc2.parent_doc,top_doc=parentdoc.top_doc,status=1).order_by('sort')
                        parent_list2 = [d.id for d in parents2]
                    except:
                        return None
                    if parent_list2.index(parentdoc2.id) == len(parent_list2) - 1:
                        next_doc = None
                        return next_doc
                    else:
                        next_id = parent_list2[parent_list2.index(parentdoc2.id) + 1]
                        return next_id
                else:
                    next_id = parent_list[parent_list.index(parentdoc.id) + 1]
                    return next_id
            else:
                next_id = docs_list[docs_list.index(doc.id) + 1]
                next_doc = Doc.objects.get(id=next_id)
                # print("下一篇：", next_doc.id, next_doc)
                return next_doc.id
        # 存在下级手册
        else:
            # 下一篇手册为下级第一篇手册
            next_doc = subdoc.order_by('sort')[0]
            # print("下一篇：", next_doc.id, next_doc)
            return next_doc.id
    except Exception as e:
        import traceback
        print(traceback.print_exc())

# 获取手册的上一篇手册
@register.filter(name='get_doc_previous')
def get_doc_previous(value):
    try:
        doc_id = value
        doc = Doc.objects.get(id=int(doc_id))  # 当前手册
        docs = Doc.objects.filter(parent_doc=doc.parent_doc,top_doc=doc.top_doc,status=1).order_by('sort')  # 同级所有手册
        docs_list = [d.id for d in docs]
        # 手册为同级中的第一个，
        if docs_list.index(doc.id) == 0:
            # 如果其为顶级手册，那么没有上一篇手册，
            if doc.parent_doc == 0:
                # print("无上一篇手册")
                previous = None
                return previous
            # 如果其为次级手册，那么其上一篇手册为上级手册
            else:
                previous = Doc.objects.get(id=doc.parent_doc)  # 获取
                # print("上一篇：", previous.id, previous)
                return previous.id
        # 手册为同级中的非第一个，那么上一篇为索引号的前一个手册
        else:
            previou_id = docs_list[docs_list.index(doc.id) - 1] # 获取前一个手册的ID
            previous = Doc.objects.get(id=previou_id) # 获取前一个手册
            # 查询以此手册为上级的手册
            previous_subdoc = Doc.objects.filter(parent_doc=previous.id,top_doc=doc.top_doc,status=1).order_by('-sort')
            # 如果没有手册以此手册为上级手册，那么为上一篇手册
            if previous_subdoc.count() == 0:
                return previou_id
            else:# 否则，上一篇手册为以此手册作为上级手册的手册里面的最后一篇手册
                previous = previous_subdoc[:1][0]
                parent_list = Doc.objects.filter(parent_doc=previous.id,top_doc=doc.top_doc,status=1).order_by('-sort')
                if parent_list.count() == 0:
                    return previous.id
                else:
                    previous = parent_list[:1][0]
                    return previous.id
    except Exception as e:
        import traceback
        print(traceback.print_exc())


# 获取内容的关键词上下文
@register.filter(name='get_key_context')
def get_key_context(value,args):
    # print(value,args)
    # re_result = re.findall(args, value, flags=re.IGNORECASE)
    value = value.replace('\n','')
    p = re.compile(args,flags=re.IGNORECASE)
    value_list = []
    for m in p.finditer(value):
        # print(value,m,m.start(),m.group(),)
        # print( m.start(), m.group())
        start_point = m.start() - 20
        if start_point < 0:
            start_point = 0
        end_point = m.end()+20
        # print(start_point,end_point)
        # print(value[start_point:end_point])
        value_list.append(value[start_point:end_point])
    # print(value_list)
    if len(value_list) > 0:
        r = "…".join(value_list)
        if len(r) > 200:
            r = r[0:200]
    else:
        r = value[0:200]
    return r