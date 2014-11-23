#coding:utf-8
class Language:
      def __init__(self):
            self.selectEN =  { # fake array of posts
             # fake array of posts
            'Home': "Home",
            'Projects': 'Projects',
            'Biopedia': 'Biopedia',
            'Login':'Login',
            'Register':'Register',
            'login_title':'Login with Biopedia Account',
            'username':'Username',
            'Password':'Password',
            'CLOSE':'close',
            'regi_title':'Register New Biopedia Account',
            'name_First':'First Name',
            'name_Last':'Last Name',
            'Email':'Email',
            'con_password':'Confirm Password',
            'Star':'Star',
            'Delete':'Delete',
            'M_F':'Mapping File',
            'S_F':'Sample File',
            'OK':'OK',
            'pro_title':'Biopedia - Projects',
            'User_info':'User Information',
            'Full_name':'Full Name',
            'mdf_pass':'MODIFY PASSWORD',
            'star_pro':'Starred Projects',
            'new_pass':'New Password',
            'modify':'MODIFY',
            'create_Project':'Created Projects',
            'Desprition':'We need a description for every project.',
            'U_Profile':'User Profile',
            'Logout':'Logout',
            'profile':'Profile'
            }

            self.selectCN = { # fake array of posts
            'Home': U"主页",
            'Projects': U'项目',
            'Biopedia': U'未命名',
            'Login':U'登录',
            'Register':U'注册',
            'title':U'在线生物信息学数据中心-Biopedia',
            'login_title':U'使用Biopedia账号登录',
            'username':U'用户名',
            'Password':U'密码',
            'CLOSE':U'关闭',
            'regi_title':U'注册新的Biopedia账号',
            'name_First':U'名',
            'name_Last':U'姓',
            'Email':U'电子邮件',
            'con_password':U'确认密码',
            'Star':U'赞',
            'Delete':U'取消',
            'M_F':U'映像文件',
            'S_F':U'样本文件',
            'OK':U'确认',
            'pro_title':U'Biopedia-项目',
            'User_info':U'用户信息',
            'Full_name':U'全名',
            'mdf_pass':U'修改密码',
            'star_pro':U'喜欢的项目',
            'new_pass':U'新密码',
            'modify':U'修改',
            'create_Project':U'创建的项目',
            'Desprition':U'请描述你的项目。',
            'U_Profile':U'个人信息',
             'Logout':U'登出',
             'profile':U'个人简介'
            }

      def selectLanguage(self, xlanguage):
            
            if xlanguage == 'cn':
                  return self.selectCN

            else:
                  return self.selectEN

