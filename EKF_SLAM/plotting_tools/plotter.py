import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from scipy import stats

def plot_landmarks(landmarks,color='k',marker='*'):
    ax = plt.gca()
    ax.scatter(landmarks['x'].values,landmarks['y'].values,c='r',marker='*',label='Ground Truth')


def draw_ellipse(position, covariance, alpha = 0.9, ax=None, **kwargs):
    """Draw an ellipse with a given position and covariance"""
    ax = ax or plt.gca()
    
    # Extracting Values
    sxx = covariance[0][0]    # sigmax
    syy = covariance[1][1]    # sigmay
    sxy = covariance[0][1]    # sigmaxy
    #print(sxx,syy,sxy)

    # Calculating EigenValues : Since this is 2x2 matrix, calculating eigenvalues is easy.
    # if lamda is the eigenvalue, then we have to solve the following equation:
    # lambda**2 - lambda(sxx+syy) + sxxsyy - sxy**2
    # so solution to the equation above using lambda = (-b +- sqrt(b**2 - 4ac))/2a is,
    # lambda = 0.5(sxx+syy +- sqrt((sxx+syy)**2 - 4sxxsyy - 4 sxy**2))
    # ==> lambda = 0.5(sxx+syy +- sqrt((sxx-syy)**2 + 4 sxy**2))
    # Now the half length of the major and minor axis coorespond to the root of the largest and smaller
    # eigenvalues.

    major = np.sqrt(0.5*(sxx+syy + np.sqrt((sxx-syy)**2 +4*sxy**2)))
    minor = np.sqrt(0.5*(sxx+syy - np.sqrt((sxx-syy)**2 +4*sxy**2)))
    
    # Checking the case when roots are imaginary.
    # If any of the eigenvalues are negative, the ellipse turns into a line.

    major = major.real
    minor = minor.real
    
    # Now we want to the ellipse to be big enough to display atleast a 'alpha' probability.
    # We use chi square distribution to find the critical value and scale it to that probability.
    critical_value = stats.chi2.ppf(alpha,2)    # Since we have two variables, degrees of freedom = 2.
    
    # We scale the axes by multiplying them by the sqrt(critical_value)
    scale_factor = np.sqrt(critical_value)
    major = major*scale_factor
    minor = minor*scale_factor
    
    # Angle is found by 0.5*taninv(2*sxy/(sxx - syy))
    angle = np.degrees(0.5*np.arctan2(2*sxy,(sxx-syy)))
    
    # Since we consider the angle between the major axis and x axis,
    # the width parameter of Ellipse function should always be the major axis.

    if major > minor:
        width = major
        height = minor
    else:
        width = minor
        height = major
        
    # Drawing ellipse.
    ax.add_patch(Ellipse(position,width=width,height=height,angle=angle,fill=False,lw=0.5,alpha=0.6,label='prob'))
    

# Plotting Robot,

def plot_robot(x,y,theta,covariance, prob,color='r'):
    radius = 0.2

    # Finding points to show orientation
    head_x = x + radius*np.cos(theta)
    head_y = y + radius*np.sin(theta)

    # Robot's body a circle.
    robot_circle = plt.Circle((x,y),radius,color=color,fill=False,label='body')

    ax = plt.gca()
    
    # Line to show orientation
    ax.plot([x,head_x],[y,head_y],color = 'b',label='orientation')
    ax.add_artist(robot_circle)

    # robot's isocontour. (probability ellipse)
    draw_ellipse((x,y),covariance,alpha=prob,fill=False)
    
    plt.xlim(-2,12)
    plt.ylim(-2,12)
    
def plot_estimated_landmarks(mu,sigma,observedLandmarks,ids,prob):
    ax = plt.gca()

    # a loop to display the estimated positions of each landmarks.
    # Also, the landamrks observed in a given timestep shown by black lines
    # from the robot to the landmarks

    # An isocontour for landmark estimations are also shown.
    for i,(x,y) in enumerate(zip(mu[3::2],mu[4::2])):
        if(observedLandmarks[i] != 0):
            ax.plot(x,y,'bo',label='estimates')
            draw_ellipse((x,y),sigma[i*2+3:i*2+5,i*2+3:i*2+5],alpha=prob,fill=False)
            if(i+1 in ids):
                ax.plot([mu[0],x],[mu[1],y],color='r',linewidth=0.4,label='sense')

def plot_and_save_state(mu,sigma,observedLandmarks,landmarks,ids,i,prob = 0.95):
    # clear figure
    plt.clf()

    # plot robot, landmarks, estimated landmarks
    plot_robot(mu[0],mu[1],mu[2],sigma[0:2,0:2],prob=prob)
    plot_landmarks(landmarks)
    plot_estimated_landmarks(mu,sigma,observedLandmarks,ids,prob=prob)
    plt.xlabel('x',size=12)
    plt.ylabel('y',size=12)
    plt.title('Timestep : {}, Confidence : {:.2f}%'.format(i+1,prob*100))
    plt.legend()
    # save figure to file
    plt.savefig('plots/ekf_{:>03}'.format(i+1))
