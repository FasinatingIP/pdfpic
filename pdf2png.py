# -*- coding: utf-8 -*-
"""
Created on Thu May 25 11:46:01 2023

@author: pan
"""
#pip install PyMuPDF
import streamlit as st
import fitz
import img2pdf #导入img2pdf库， 安装命令：pip install img2pdf
from io import BytesIO
from PIL import Image, ImageEnhance
import zipfile
#print(os.__version__)
#print(fitz.__doc__)
#全局配置
st.set_page_config(
    page_title="pdfpic",    #页面标题
    page_icon=":framed_picture:",       #icon:emoji":rainbow:             
    initial_sidebar_state="auto"  #侧边栏
)

def readuploadimg(upload_file):
    # To read file as bytes:
    bytes_data = upload_file.getvalue()
    #将字节数据转化成字节流
    bytes_data = BytesIO(bytes_data)
    #Image.open()可以读字节流
    img = Image.open(bytes_data)
    return img

def readuploadpdf(pdf_file):
    bytes_data = pdf_file.getvalue()
    pdfDoc = fitz.open(stream=bytes_data)
    return pdfDoc

tab1, tab2, tab3 = st.tabs(["pdf转图片", "图片转pdf","合并长图" ])
@st.cache_data
def pdf2png(pdf_file,dpi,outtype):
    bytes_data = pdf_file.getvalue()
    pdfDoc = fitz.open(stream=bytes_data)
    filename=pdf_file.name[:pdf_file.name.rindex(".")]
    zipname=filename+'.zip'
    page_num = 1
    with zipfile.ZipFile(zipname,'w') as z:
        for page in pdfDoc:
            #rotate = int(0)
            pdfDoc=readuploadpdf(pdf_file)
            mat = fitz.Matrix()
            pixmap = page.get_pixmap(matrix=mat, alpha=False,dpi=dpi)
            output_filename=f"{filename}-{page_num}.{outtype}"
            pixmap.pil_save(output_filename)
            st.markdown(f"第{page_num}张图片已生成！")
            page_num = page_num + 1 
            z.write(output_filename)
    return output_filename,zipname,page_num
#pdf2png
with tab1:
    #界面
    with st.form("pdf2pic"):
        dpi=st.number_input(label='输入dpi,值越大，越清晰',value=200,key="dpi")
        outtype = st.selectbox('输出的图片类型',('png', 'jpg'))
        # 上传pdf文件
        pdf_file = st.file_uploader("请选择要上传的PDF或拖拽文件至下方区域！",
                                         type=['pdf'],accept_multiple_files=False)
        submitted = st.form_submit_button("点我开始转换")
    #st.write(pdf_file.name)
    if pdf_file is not None:
        output_filename,zipname,page_num=pdf2png(pdf_file,dpi,outtype)
        st.success("全部转换成功！")
        #只有一页的直接下载图片，一页以上的下载压缩包
        if page_num==2:
            with open(output_filename, "rb") as file:
                btn=st.download_button(
                    label="点我下载图片",
                    data=file,
                    file_name=output_filename,
                    mime="image/"+outtype
                    
                    )
        elif page_num>2:
            #下载本地图片
            with open(zipname, "rb") as file:
                btn = st.download_button(
                    label="点我下载zip",
                    data=file,
                    file_name=zipname,
                    mime="application/zip",
                    key='zip'
                    )
        else:
            st.error('请上传有效文件！')
    else:
        st.warning("请上传文件！")

#png2pdf    
with tab2:
    #界面
    with st.form("png2pdf"):
        output_filename =st.text_input(label="输出的文件名",value="output")
        # 上传图像
        image_files = st.file_uploader("(支持多张！！)请选择要上传的图片或拖拽文件至下方区域！",
                                         type=['jpg','png'],accept_multiple_files=True)
        out_file=output_filename+".pdf"
        submitted = st.form_submit_button("点我开始转换")
    
    if submitted:
        if len(image_files)>0:
            imgs=[]
            for image in image_files:
                bytes_data = image.getvalue()
                #将字节数据转化成字节流
                img = BytesIO(bytes_data)
                imgs.append(img)
        
            with open(out_file, 'wb+') as f: 
                f.write(img2pdf.convert(imgs))
            with open(out_file, "rb") as file:
                btn = st.download_button(
                    label="点我下载pdf",
                    data=file,
                    file_name=out_file,
                    key='png2pdf'
                    )
        else:
            st.warning("请上传图片集！")
        
#合并长图        
with tab3:
    
    #界面
    with st.form("concatpic"):
        output_filename =st.text_input(label="输出的文件名",value="output")
        lpictype = st.selectbox('输出的图片类型',('.png', '.jpg'),key="lpictype")
        # 上传图像
        image_files = st.file_uploader("(支持多张！！)请选择要上传的图片或拖拽文件至下方区域！",
                                         type=['jpg','png'],accept_multiple_files=True)
        output_file=output_filename+lpictype
        submitted = st.form_submit_button("点我开始转换")
    
    if submitted:
        
        if len(image_files)>0:
            ims=[]
            for uploaded_file in image_files:
                img=readuploadimg(upload_file=uploaded_file)
                ims.append(img)
            ims_size = [list(im.size) for im in ims]
            middle_width = sorted(ims_size, key=lambda im: im[0])[int(len(ims_size)/2)][0]  # 中位数宽度
            ims = [im for im in ims if im.size[0] > middle_width/2]  # 过滤宽度过小的无效图片
             
            # 过滤后重新计算
            ims_size = [list(im.size) for im in ims]
            middle_width = sorted(ims_size, key=lambda im: im[0])[int(len(ims_size)/2)][0]  # 中位数宽度
            ims = [im for im in ims if im.size[0] > middle_width/2]  # 过滤宽度过小的无效图片
             
            # 计算相对长图目标宽度尺寸
            for i in range(len(ims_size)):
                rate = middle_width/ims_size[i][0]
                ims_size[i][0] = middle_width
                ims_size[i][1] = int(rate*ims_size[i][1])
             
            sum_height = sum([im[1] for im in ims_size])
            # 创建空白长图
            result = Image.new(ims[0].mode, (middle_width, sum_height))
             
            # 拼接
            top = 0
            for i, im in enumerate(ims):
                mew_im = im.resize(ims_size[i], Image.ANTIALIAS)  # 等比缩放
                result.paste(mew_im, box=(0, top))
                top += ims_size[i][1]
            # 保存
            result.save(output_file)
        
            #下载本地图片
            with open(output_file, "rb") as file:
                btn = st.download_button(
                    label="点我下载图片",
                    data=file,
                    file_name=output_file,
                    mime="image/png",
                    key='concatpic'
                    )
            
            #显示图片
            st.image(result)
            
        else:
          st.warning("请上传图片集！")
          
        
        

            

            
    