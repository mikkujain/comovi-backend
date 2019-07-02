from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.template.loader import get_template
from django.template import Context
class MailManager():
	def __init__(self):
		self.sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
		self.from_email = settings.SENDGRID_FROM_EMAIL

	def send_welcome(self, email_id, property_name, name, content, link):
		template = get_template('email/welcome.html')
		context = {
			'property_name' : property_name,
			'name' : name,
			'link' : link,
			'content': content,
			}
		context['content'] = context['content'].replace('Name', name)
		context['content'] = context['content'].replace('property_name', property_name)
		context['content'] = context['content'].replace('Login', link)	
		email_content = template.render(context)
		mail = Mail(
			from_email=self.from_email,
			to_emails=email_id,
			subject='Welcome to {}'.format(property_name),
			html_content=email_content
			)

		resp = self.sg.send(mail)
		return True

	def send_forgot_password(self, email_id, name, new_password, content, link):
		template = get_template('email/forgot_password.html')
		context = {
			'name' : name,
			'new_password' : new_password,
			'link' : link,
			'content': content,
			}
		context['content'] = context['content'].replace('Name', name)
		context['content'] = context['content'].replace('new_password', new_password)
		context['content'] = context['content'].replace('Login', link)
		email_content = template.render(context)
		mail = Mail(
			from_email=self.from_email,
			to_emails=email_id,
			subject='Forgot Password',
			html_content=email_content
			)
		resp = self.sg.send(mail)
		return True

	def send_new_message(self, email_id, name, from_name, message, content): 
		template = get_template('email/new_message.html')
		context = {
			'name' : name,
			'from_name' : from_name,
			'message' : message,
			'content' : content,
			}
		context['content'] = context['content'].replace('Name', from_name )
		context['content'] = context['content'].replace('Text', message )

		email_content = template.render(context)
		mail = Mail(
			from_email=self.from_email,
			to_emails=email_id,
			subject='New Message',
			html_content=email_content
			)
		resp = self.sg.send(mail)
		print(resp.status_code)
		print("email sent")
		return True

	def send_new_notice(self, email_id, name, title, body, content):
		template = get_template('email/new_notice.html')
		context = {
			'name' : name,
			'title' : title,
			'body' : body,
			'content': content,
			}

		context['content'] = context['content'].replace('Name', name)
		context['content'] = context['content'].replace('title', title)
		context['content'] = context['content'].replace('Text', body)
		email_content = template.render(context)
		mail = Mail(
			from_email=self.from_email,
			to_emails=email_id,
			subject='There is a new notice on the Mural Newspaper',
			html_content=email_content
			)
		resp = self.sg.send(mail)
		return True

	def send_new_condonium_user(self, email_id, name, property_name, password, content, link):
		template = get_template('email/new_condonium_user.html')
		context = {
			'name' : name,
			'property_name' : property_name,
			'password' : password,
			'link' : link,
			'content': content,
			}

		context['content'] = context['content'].replace('Name',name)
		context['content'] = context['content'].replace('property_name',property_name)
		context['content'] = context['content'].replace('password',password)
		context['content'] = context['content'].replace('Login',link)
		email_content = template.render(context)
		mail = Mail(
			from_email=self.from_email,
			to_emails=email_id,
			subject='Welcome to \"{}\"'.format(property_name),
			html_content=email_content
			)
		resp = self.sg.send(mail)
		print(resp.status_code)
		print("email sent")
		return True
