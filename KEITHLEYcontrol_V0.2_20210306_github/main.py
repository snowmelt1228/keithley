#导入VISA通讯库
import visa
#PYTHON时间库
import time
#KEITHLEY设备source meter支持文件，一定要和本程序放在一起
import SmuPy_20190807 as kei

# ===== MAIN PROGRAM STARTS HERE =====

#检查时间
t1 = time.time()
#建立VISA管理
rm = visa.ResourceManager() 	# Opens the resource manager and sets it to variable rm
#给出设备ID
#smu_id_1 = "USB0::0x05E6::0x2602::4132104::INSTR"
#在我的电脑上是用RS232转USB连接电脑，是串口serial，语句用最后一项，设备管理器可见是COM3，数字用3
smu_id_1 = "ASRL3::INSTR"

'''#根据连接方式不同，应该采用的设备ID举例
# Instrument ID String examples...
#       LAN -> TCPIP0::134.63.71.209::inst0::INSTR
#       USB -> USB0::0x05E6::0x2450::01419962::INSTR
#       GPIB -> GPIB0::16::INSTR
#       Serial -> ASRL4::INSTR'''

#设置超时
timeout = 20000
#my_file = "DiodeTestFunctions_12Jun2019.tsp"
#建立支持库
my_smu = kei.SmuPy()
#连接设备
my_smu.instrument_connect(rm, smu_id_1, timeout, 1, 1, 1)
#my_smu.load_script_file(my_file)
#发出命令，让蜂鸣器响一下,参量为时间，频率
my_smu.instrument_write("beeper.beep(1,300)")
#在A通道设置为1V电压
my_smu.instrument_write('smua.source.levelv = 1')
#发出输出电压命令
my_smu.instrument_write('smua.source.output = smua.OUTPUT_ON')
#等待60s
time.sleep(60)
#在A通道设置为0V电压
my_smu.instrument_write('smua.source.levelv = 0')
#发出停止输出电压命令
my_smu.instrument_write('smua.source.output = smua.OUTPUT_OFF')
#发出命令，让蜂鸣器响一下
my_smu.instrument_write("beeper.beep(1,300)")
#解除连接
my_smu.instrument_disconnect()
#检查时间
t2 = time.time()

'''
补充说明：
用RS232转USB把KEITHLEY设备接上电脑，查看设备管理器确认设备接口编号，确定通道名称
程序运行需要
1 python有VISA模块，有labview2014及NI6363安装，以保证有NI-VISA和IVI driver
2 有SmuPy_20190807.py文件放在一起
3 把通道名称smu_id_1写对
可能问题：
1 可以使用的命令见2600AS-901-01--E-Aug2011--Ref.pdf 里面的 command reference 一章
2 RS232连接，需要保证计算机和KEITHLEY设备连接参数是一致的。
计算机设置在设备管理器，右键选择该设备的属性；KEITHLEY在MENU设置的RS232里面
通常采用9600每秒位数，8数据位，无奇偶校验，1停止位，无流控制
'''