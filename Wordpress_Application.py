import tkinter as tk
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from PIL import ImageTk,Image  
from tkinter import messagebox
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import *
from wordpress_xmlrpc.methods.users import *
from wordpress_xmlrpc.compat import *
from wordpress_xmlrpc.methods import *
import os
import json

imgArg = sys.argv[1] #this will get the image path as argument
print (imgArg) #path of the image

#Function to get the image size to show in the tkinter window
def getHeightForWidth(widthInt):
	wpercent = (widthInt/float(Image.open(imgArg).size[0]))
	hsize = int((float(Image.open(imgArg).size[1])*float(wpercent)))
	return hsize

#main window - TOP
root = tk.Tk() 
root.title("Wordpress Tool - Vijayatm") #window title

#Title Section
tk.Label(root,text="Title of the post").grid(row=0)
title_entry = tk.Entry(root)
title_entry.grid(row=1)

#Image Section
imageHolder = ImageTk.PhotoImage(Image.open(imgArg).resize([300,getHeightForWidth(300)],Image.ANTIALIAS))
imgLabel = Label(root,image=imageHolder).grid(row=2)

tk.Label(root, text="Enter the content of your blog post: ").grid(row=3)
description_entry = ScrolledText(root,width=40,height=5)
description_entry.grid(row=4)

def showText():
	title = title_entry.get()
	description = description_entry.get('1.0',END)

	isYes = messagebox.askyesno("Confirmation to post", "Are you sure you want to post?")
	if isYes:
		print("Title: {titleKey} \nDescrption: {descriptionKey}".format(titleKey=title,descriptionKey=description))
		wp = Client('https://vijayatm.wordpress.com/xmlrpc.php', 'yourUserName', 'yourPassword') #replace your username and password here
		data = {
		'name': 'Python file Name.jpg',
		'type': 'image/jpg'}
		with open (imgArg, 'rb') as img:
			data['bits'] = xmlrpc_client.Binary(img.read())
		response = wp.call(media.UploadFile(data))
		attachmentURL = response['url']
		attachmentID = response['attachment_id']
		print (response)
			
		post = WordPressPost()
		post.title = title
		post.content = "<img src='{att1}'/><br>{description}".format(att1=attachmentURL,description=description)
		post.thumbnail = attachmentID
		post.terms_names={
			'post_tag':['vijayatm','usingPython','tkinter','wordpress']
		}
		post.post_status='publish'
		resp = wp.call(NewPost(post))
		print(resp)
		root.destroy()
	else:	
		messagebox.showinfo('Welcome Back','Update the description if you want to')

button = tk.Button(text="Post it", command=showText,highlightbackground='#3E4149').grid(row=5)
root.mainloop()	
