--ds18b20温度读取回调函数
function readout(temp)
  for addr, tmp in pairs(temp) do
    tmp0=tmp
  end
end

--通过串口控制模块发送数据
--必须使用玄学方法，用tmr.delay会卡爆，应该是看门狗杀死的
function senduart()
    uart.write(1,"\r\nAT+CIPMODE=1\r\n")
    print("Wait CIPMODE")
    tmr.create():alarm(1000,tmr.ALARM_SINGLE,function()
        print("Wait Connect")
        uart.write(1,'AT+CIPSTART="TCP","114.55.93.225",2333\r\n')
        tmr.create():alarm(20*1000,tmr.ALARM_SINGLE,function()
            uart.write(1,s.."\r\n")
            print("Send to server ok")
            status=1
        end)
    end)
end

function sendtemp()
    --等待dnt11
    dhtstatus=-1
    while dhtstatus~=dht.OK do
    dhtstatus, tmp1, humi, temp_dec, humi_dec = dht.read11(6)
    end
    
    --等待bmp温度
    tmp2=-1000
    while tmp2<-500 do
    tmp2=bmp085.temperature()
    end
    
    --等待bmp压强
    pres=-100
    while pres<0 do
    pres=bmp085.pressure()
    end
    
    --等待ds18b20温度，nodemcu调用这个模块不大聪明的亚子
    if(tmp0==-100)then
        print("Waiting %d",tmp0)
        t:read_temp(readout, 5, t.C)
        tmr.create():alarm(1000,tmr.ALARM_SINGLE,sendtemp)
    else
        s=tmp0.."/"..tmp1.."/"..humi.."/"..(tmp2/10)..'.'..(tmp2%10)..'/'..pres
        print(s)
        senduart()
    end
end


--初始化ds18b20和i2c
t = require("ds18b20")
tmp0=-100
t:read_temp(readout,5,t.C)

i2c.setup(0,2,1,i2c.SLOW)
bmp085.setup()

--延时保证通信模块初始化完成

--开始发送，延时以保证通信模块初始化完全
status=0
tmr.create():alarm(30*1000,tmr.ALARM_SINGLE,sendtemp)

--深度睡眠
tmr.create():alarm(1000,tmr.ALARM_AUTO,function()
    if(status==1)then
        print("GN")
        node.dsleep(9*60*1000*1000)
    end
end
)
