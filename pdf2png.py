# -*- coding: utf-8 -*-
"""
Created on Thu May 25 11:46:01 2023

@author: pan
"""
#pip install PyMuPDF
import streamlit as st
import fitz
import datetime
import os
import img2pdf #导入img2pdf库， 安装命令：pip install img2pdf
import shutil
#print(os.__version__)
#
tab1, tab2, tab3, tab4, tab5 = st.tabs(["pdf转图片", "图片转pdf", "pdf清晰度加强","图像清晰度加强","合并长图"])
#pdf2png
with tab1:
    @st.cache_data
    def pdf2png(pdfPath,dpi,outtype):
            startTime_pdf2img = datetime.datetime.now()  # 开始时间
            #获取文件名生成导出文件夹名
            outpath =pdfPath[:pdfPath.rindex(".")]
            #d:/filename
            filename=pdfPath[(pdfPath.rindex("/")+1):pdfPath.rindex(".")]

            if not os.path.exists(outpath):
                os.makedirs(outpath)
            pdfDoc = fitz.open(pdfPath)
            page_num = 1
            for page in pdfDoc:
                #rotate = int(0)
                mat = fitz.Matrix()
                pixmap = page.get_pixmap(matrix=mat, alpha=False,dpi=dpi)
                
                pixmap.pil_save(f"{outpath}/{filename}-{page_num}.{outtype}")
                
                st.markdown(f"第{page_num}张图片保存完成")
                page_num = page_num + 1 
            return outpath
            endTime_pdf2img = datetime.datetime.now()  # 结束时间
            st.write('花费时间=', (endTime_pdf2img - startTime_pdf2img).seconds)
    #界面
    dpi=st.number_input(label='输入dpi,值越大，越清晰',value=300,key="dpi")
    outtype = st.selectbox('输出的图片类型',('png', 'jpg'))
    
    pdfPath = st.text_input(label="输入文件路径，例：d:/文件名.pdf",value="",key="pdf2png")
    
    #pdfPath="d:/德龙304材质书4.13(13709)第三页12行.pdf"
    if pdfPath != "":
        if (pdfPath[(pdfPath.rindex(".")+1):]=="pdf") & (os.path.exists(pdfPath)):
            #st.write(pdfPath)
            outpath=pdf2png(pdfPath=pdfPath,dpi=dpi,outtype=outtype)
            st.success('文件导出在'+outpath) 
            agree = st.checkbox('是否打开所在文件夹')
            if agree:
                os.startfile(outpath)
            else:
                pass
            
        else:
            st.error("请输入已存在的pdf格式的文件路径")
    else:
     	st.warning("请填写文件路径！")

#png2pdf    
with tab2:    
    @st.cache_data
    def png2pdf(imgpath,pictype):
       outfile=imgpath+'-1.pdf'  
       try:         
           with open(outfile, 'wb+') as f:   #创建以二进制读写模式 ‘PDF‘’加时间戳的PDF文件
               imgs =[] #创建图片路径保存列表
               for fname in os.listdir(imgpath): #遍历图片文件夹里面的文件
                   if not fname.endswith(tuple(pictype.split("/"))): #遍历文件格式为jpg的图片文件
                       continue
                   path = os.path.join(imgpath, fname) #读取图片文件路径
                   if os.path.isdir(path):
                       continue
                   imgs.append(path)  #添加图片路径到imgs列表
               f.write(img2pdf.convert(imgs)) #转换imgs列表里面所有图片为一个PDF文件
           return outfile
       except OSError as err:
           st.error("OS error: {0}".format(err))  #打印转换出错
     
    #界面
    
    
    pictype = st.selectbox('输入的图片类型',('.png/.jpg','.png', '.jpg'),key="pictype")
    imgpath = st.text_input(label="输入图片所在文件夹的路径，例：d:/文件夹",value="")
    #imgpath = 'D:\青泰加工单  1607+1608（原7104）'  #设置图片文件夹
    if imgpath != "":
        if (os.path.exists(imgpath)):
            outfile=png2pdf(imgpath=imgpath,pictype=pictype)
            st.success('文件导出在'+outfile) 
            openpdf = st.checkbox('是否打开pdf文件')
            if openpdf:
                os.startfile(outfile)
            else:
                pass
        else:
            st.error("请输入已存在的文件夹路径")
    else:
     	st.warning("请填写文件路径！")
         
with tab3:
    @st.cache_data
    def pdf2pdf(pdfPath,dpi):
            outtype="png"
            #获取文件名生成导出文件夹名
            outpath_o =pdfPath[:pdfPath.rindex(".")]
            outpath =outpath_o+"zzzhhh"
            #d:/filename
            filename=pdfPath[(pdfPath.rindex("/")+1):pdfPath.rindex(".")]

            if not os.path.exists(outpath):
                os.makedirs(outpath)
            pdfDoc = fitz.open(pdfPath)
            
            page_num = 1
            for page in pdfDoc:
                #rotate = int(0)
                mat = fitz.Matrix()
                pixmap = page.get_pixmap(matrix=mat, alpha=False,dpi=dpi)
                pixmap.pil_save(f"{outpath}/{filename}-{page_num}.{outtype}")
                page_num = page_num + 1 
            outfile=outpath_o+'-1.pdf' 
            
            imgpath=outpath
            try:         
                with open(outfile, 'wb+') as f:   #创建以二进制读写模式 ‘PDF‘’加时间戳的PDF文件
                    imgs =[] #创建图片路径保存列表
                    for fname in os.listdir(imgpath): #遍历图片文件夹里面的文件
                        if not fname.endswith(outtype): #遍历文件格式为jpg的图片文件
                            continue
                        path = os.path.join(imgpath, fname) #读取图片文件路径
                        if os.path.isdir(path):
                            continue
                        imgs.append(path)  #添加图片路径到imgs列表
                    f.write(img2pdf.convert(imgs)) #转换imgs列表里面所有图片为一个PDF文件
         
            except OSError as err:
                st.error("OS error: {0}".format(err))  #打印转换出错
            #删除中转的图片文件夹
            try:
                shutil.rmtree(imgpath)
            except OSError as e:
                st.write("Error: %s - %s." % (e.filename, e.strerror))
            return outfile
    #界面
    dpi=st.number_input(label='输入dpi,值越大，越清晰',value=300,key="changedpi")
    
    pdfpath = st.text_input(label="输入文件路径，例：d:/文件名.pdf",value="",key="pdf2pdf")
    #dpi=300
    #pdfPath="d:/德龙304材质书4.13(13709)第三页12行.pdf"
    if pdfpath != "":
        if (pdfpath[(pdfpath.rindex(".")+1):]=="pdf") & (os.path.exists(pdfpath)):
            #st.write(pdfPath)
            outfile=pdf2pdf(pdfPath=pdfpath,dpi=dpi)
            st.success('文件导出在'+outfile) 
            agree = st.checkbox('是否打开转换后的文件')
            if agree:
                os.startfile(outfile)
            else:
                pass
            
        else:
            st.error("请输入已存在的pdf格式的文件路径")
    else:
     	st.warning("请填写文件路径！")  

#图像增强
with tab4:
    from PIL import Image, ImageEnhance
    from io import BytesIO 
    factor=st.number_input(label='设置增强因子，值越大则图像的清晰度越高',value=2,key="factor")
    # 打开原图像
    uploaded_file = st.file_uploader("请选择要上传的图片或拖拽文件至下方区域！")
    #img = Image.open('D:/青泰加工单  1607+1608（原7104）/青泰加工单  1607+1608（原7104）-1.png')
    
    
    if uploaded_file is not None:
     # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        #将字节数据转化成字节流
        bytes_data = BytesIO(bytes_data)
        #Image.open()可以读字节流
        img = Image.open(bytes_data)
    
        # 设置增强因子
        enhancer = ImageEnhance.Sharpness(img)
        #factor = 2.0
         
        # 增强图片
        img_enhanced = enhancer.enhance(factor)
         
        # 保存增强后的图像
        output_en="增强"+uploaded_file.name
        img_enhanced.save(output_en)
        
        #下载本地图片
        with open(output_en, "rb") as file:
            btn = st.download_button(
                label="点我下载图片",
                data=file,
                file_name=output_en,
                mime="image/png"
                )
            
with tab5:
    import math
    @st.cache_data
    def merge_images(image_folder, output_file, n):
        # 获取所有图像文件的列表
        image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith('.png')]
     
        # 计算每个小图像的大小和大图像的大小
        image_count = len(image_files)
        if image_count == 0:
            print('No image files found in the directory:', image_folder)
            return
     
        # 计算小图像的大小以及大图像的大小
        img = Image.open(image_files[0])
        img_size0 = img.size[0]
        img_size1 = img.size[1]
        new_img_size0 = img_size0 * n
        new_img_size1 = img_size1 * math.ceil(len(image_files)/n)
     
        # 创建一个新的大图像
        new_img = Image.new('RGB', (new_img_size0, new_img_size1), 'white')
     
        # 将所有小图像粘贴到新图像的正确位置
        for i, f in enumerate(image_files):
            row = int(i / n)
            col = i % n
            img = Image.open(f)
            img = img.resize((img_size0, img_size1))
            new_img.paste(img, (col * img_size0, row * img_size1))
     
        # 保存大图像
        new_img.save(output_file)
     
     
    # 用法示例
    image_folder =st.text_input(label="输入图片所在文件夹的路径，例：d:/文件夹",value="",key="image_folder")
    output_filename =st.text_input(label="输出的文件名",value="output")
    lpictype = st.selectbox('输入的图片类型',('.png', '.jpg'),key="lpictype")
    n=st.number_input(label='每行显示的图像数',value=1,key="colnum")
    output_file=output_filename+lpictype
    if os.path.exists(image_folder):
        merge_images(image_folder, output_file, n)
        st.success("转换成功！")
        #下载本地图片
        with open(output_file, "rb") as file:
            btn = st.download_button(
                label="点我下载图片",
                data=file,
                file_name=output_file,
                mime="image/png"
                )
    else:
        st.error("请输入存在的文件夹路径！")
    
    
    
            
    