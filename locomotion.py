from image import *
import rospy
from geometry_msgs.msg import Twist
from kobuki_msgs.msg import BumperEvent
from std_msgs.msg import Float64


##Global Variables Declaration

g=0
y=0
z=0
q=0
bump = False
bumpRight = False
leftTurn= False
uturnflag=False
image=1
cmd_vel = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)
file=open("datalogging.txt",'a+')


##Function block for obstacle identification

def processBump(data):
      print("bump")
      global bump
      
      bump = False
      

      if data.state==BumperEvent.PRESSED and bumpRight:

			
		uturn(325)
				
		

      elif data.state==BumperEvent.PRESSED and not bumpRight:
		print("stuck")

		bump = True

      else:
                bump = False
      
     

     

###############################################
#####Moves to opposite side of wall when endpoint reached

def uturn(throw):
      
      global move_cmd
      global uturnflag 
      uturnflag=True
      move_cmd= Twist()
      degree=throw
      global image
      global file
      t=0
      while t<10:
	         move_cmd.linear.x = -0.4
     	         move_cmd.angular.z =0
                 file.write("linear=-0.4, angular=0\n")
	         cmd_vel.publish(move_cmd)
	         r = rospy.Rate(20)
	         t+=1
	         r.sleep()
	         rospy.loginfo(t)
      camera = TakePhoto()
      img_title = rospy.get_param('~image_title', 'obstacle_%s.jpg'%image)
      image+=image
      camera.take_picture(img_title)
      t=0
      while degree>0:
                move_cmd.linear.x = 0
                move_cmd.angular.z =-0.2
                file.write("linear=0, angular=-0.2\n")
	        rospy.loginfo(degree)
      left_move_little()

def left_move_little():
      global leftTurn
      global uturnflag
      global file
      
      if not leftTurn:
	 leftTurn = True
         s=0
	 t=0

	 while t<50:
	         move_cmd.linear.x = 0.3
     	         move_cmd.angular.z =0
                 file.write("linear=0.3, angular=0\n")
	         cmd_vel.publish(move_cmd)
	         r = rospy.Rate(20)
	         t+=1
	         r.sleep()
	         rospy.loginfo(t)
         t=0		
         while t<150:
                move_cmd.linear.x = 0
                move_cmd.angular.z =-0.2
                file.write("linear=0, angular=-0.2\n")
	        cmd_vel.publish(move_cmd)
	        r = rospy.Rate(20)
	        t+=1
	        r.sleep()
	 t=0
         
         uturnflag=False
         leftTurn = False
         	      

#########################################################
## Avoids the obstacles when encountered



def turn(throw):
      print("exe")
      global q,g
      global move_cmd
      move_cmd= Twist()
      degree=throw
      g=throw
      global image
      global file
      while q<10:
	         move_cmd.linear.x = -0.4
     	         move_cmd.angular.z =0
                 file.write("linear=-0.4, angular=0\n")
	         cmd_vel.publish(move_cmd)
	         r = rospy.Rate(20)
	         q+=1
	         r.sleep()
	         rospy.loginfo(q)

      camera = TakePhoto()
      img_title = rospy.get_param('~image_title', 'obstacle_%s.jpg'%image)
      image+=image
      camera.take_picture(img_title)
      q=0
      while degree>0:
                move_cmd.linear.x = 0
                move_cmd.angular.z =-0.2
                file.write("linear=0, angular=-0.2\n")
	        cmd_vel.publish(move_cmd)
	        r = rospy.Rate(20)
	        degree-=1
	        r.sleep()
	        rospy.loginfo(degree)
      move_little()

def move_little():
      global y
      global move_cmd
      global bumpRight
      global file
      move_cmd= Twist()
      if not bumpRight:
      	while y<25 and not uturnflag:
		bumpRight = True
	        move_cmd.linear.x = 0.3
     	        move_cmd.angular.z =0
                file.write("linear=0.3, angular=0\n")
	        cmd_vel.publish(move_cmd)
	        r = rospy.Rate(20)
	        y+=1
	        r.sleep()
	        rospy.loginfo(y)
		
		

      y=0
      bumpRight = False
      turn_back()
      

def turn_back():
      global g
      global move_cmd
      move_cmd= Twist()
      global file
      if not bumpRight:

     	 while g>0 and not uturnflag:
                move_cmd.linear.x = 0
                move_cmd.angular.z =0.2
                file.write("linear=0.2, angular=0.2\n")
	        cmd_vel.publish(move_cmd)
	        r = rospy.Rate(20)
	        g-=1
	        r.sleep()
	        rospy.loginfo(g)
		

# Shutdown function
		
def shutdown():
    # stop turtlebot
    rospy.loginfo("Stop TurtleBot")
    # a default Twist has linear.x of 0 and angular.z of 0.  So it'll stop TurtleBot
    file.close()
    cmd_vel.publish(Twist())
	
	
# Main Function - Turtlebot moves	

def listener():
    rospy.init_node('laserscan', anonymous=True)
    print("listen")
    global cmd_vel
    global file
    sub=rospy.Subscriber('mobile_base/events/bumper', BumperEvent, processBump)
     # spin() simply keeps python from exiting until this node is stopped
    rospy.on_shutdown(shutdown)
    print("run")
    move_cmd= Twist()
    move_cmd.linear.x = 0.3
    move_cmd.angular.z =0

    
    while not rospy.is_shutdown():
      

      if not uturnflag:
	    

            global bump
            global bumpRight
	    if bumpRight:
		bumpRight=False
            if bump==True:
                print("turn")
                turn(150)
            print("running")
            file.write("linear=0.3, angular=0\n")
	    cmd_vel.publish(move_cmd)
	    r = rospy.Rate(20)
            r.sleep()
			
			
if __name__ == '__main__':
    try:
	        print("start")
                listener()
    except Exception as e:
		print(e)
                rospy.loginfo("GoForward node terminated.")
