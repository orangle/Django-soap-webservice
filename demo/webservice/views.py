#-*- coding: utf-8 -*-
#author: orangleliu   @2014-05-21
#python2.7.x
'''
webservice  demo
参考文章：https://gist.github.com/rotaris/935809
'''
import soaplib
from soaplib.core.service import rpc, DefinitionBase, soap
from soaplib.core.model.primitive import String, Integer
from soaplib.core.server import wsgi
from soaplib.core.model.clazz import Array
from soaplib.core.model.clazz import ClassModel


class StudentInfo(ClassModel):
    __namespace__ = "StudentInfo"
    name = String
    age = Integer
    address = String


class  StudentSoapService(DefinitionBase):
    @soap(String, _returns=String)
    def getStudent(self, name):
        try:
            print  "The student name is :%s"%name
            #TODO 处理逻辑
            res = StudentInfo()
            res.name  = 'orangleliu'
            res.age = '24'
            res.address = u'北京朝阳'
        except Exception,e:
            print str(e)
        return res


#把接口集成到django中，直接使用django来对外提供服务
from soaplib.core.server.wsgi import Application
from django.http import HttpResponse

import  StringIO
class DumbStringIO(StringIO.StringIO):
    def read(self, n):
        return self.getvalue()

class DjangoSoapApp(Application):
    def __call__(self, request):
        django_response = HttpResponse()
        def start_response(status, headers):
            status, reason = status.split(' ', 1)
            django_response.status_code = int(status)
            for header, value in headers:
                django_response[header] = value

        environ = request.META.copy()
        environ['CONTENT_LENGTH'] = len(request.raw_post_data)
        environ['wsgi.input'] = DumbStringIO(request.raw_post_data)
        environ['wsgi.multithread'] = False

        try:
            response = super(DjangoSoapApp, self).__call__(environ, start_response)
        except Exception,e:
            error = str(e)
            raise Exception(u'Get the input date exception: '+ error)

        django_response.content = '\n'.join(response)
        return django_response

#添加服务
soap_application = soaplib.core.Application([StudentSoapService], 'tns')
#urls 中配置的是这个名称
get_student_soap = DjangoSoapApp(soap_application)
