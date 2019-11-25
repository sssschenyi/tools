# -*- coding: utf-8 -*-
import pygame
import os

file_path_list=[]

def file_path(file_dir):
	for root, dirs, files in os.walk(file_dir):
		print('root_dir',root)
		mp3FileLen=len(os.listdir(file_dir))#计数mp3文件的数量
		fp = os.listdir(file_dir)
		i=0
		for files in fp:			
			tmp_path = os.path.join(file_dir,files)# string 当前路径下的文件
			file_path_list.append(tmp_path)# 将每条路径加入列表			
			print(i,":",files)
			print('')
			i+=1
		print("#########你的文件夹有%d首歌###########"%mp3FileLen)
		#print(file_path_list[130])

file_path('F:\mp3')
mp3ID=input("请输入歌曲的ID:")
print("")
mp3FileAddress=file_path_list[int(mp3ID)]
print("开始播放:",os.path.basename(mp3FileAddress))#打印当前播放的歌曲名

file=mp3FileAddress#文件名是完整路径名

pygame.mixer.init()#初始化音频

track = pygame.mixer.music.load(file)#载入音乐文件
#mp3Time=pygame.mixer.music.get_pos()#得到音乐播放时间

while True:
	if pygame.mixer.music.get_busy()==False:
		pygame.mixer.music.play(loops=10,start=0.1)#开始播放,重复播放10次
		#print(pygame.mixer.music.get_pos())

#time.sleep(6)#播放6秒
pygame.mixer.music.stop()#停止播放
