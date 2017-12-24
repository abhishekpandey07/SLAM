import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from scipy import stats

def plot_landmarks(landmarks,color='k',marker='*'):
    ax = plt.gca()
    ax.scatter(landmarks['x'].values,landmarks['y'].values,c='r',marker='*')

def draw_ellipse(position, covariance, alpha = 0.9, ax=None, **kwargs):
    """Draw an ellipse with a given position and covariance"""
    ax = ax or plt.gca()
    '''
    # Convert covariance to principal axes
    if covariance.shape == (2, 2):
        U, s, Vt = np.linalg.svd(covariance)
        angle = np.degrees(np.arctan2(U[1, 0], U[0, 0]))
        width, height = 2 * np.sqrt(s) * np.sqrt(alpha)
        print('hmm')
    else:
        angle = 0
        width, height = 2 * np.sqrt(covariance) * np.sqrt(alpha)
    for nsig in range(5, 8):
        ax.add_patch(Ellipse(position, nsig * width, nsig * height,
                             angle, **kwargs))
    '''
    
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
    #print('Major before scaling : {}'.format(major))
    #print('Minor before scaling : {}'.format(minor))
    
    # Now we want to the ellipse to be big enough to display atleast a 'alpha' probability.
    # We use chi square distribution to find the critical value and scale it to that probability.
    critical_value = stats.chi2.ppf(alpha,2)    # Since we have two variables, degrees of freedom = 2.
    
    # We scale the axes by multiplying them by the sqrt(critical_value)
    scale_factor = np.sqrt(critical_value)
    major = major*scale_factor
    minor = minor*scale_factor
    
    #print('Major after scaling : {}'.format(major))
    #print('Minor after scaling : {}'.format(minor))
    
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
        
    #print('Major = {}, Minor = {} , angle = {}'.format(major,minor,angle))
    # Drawing ellipse.
    ax.add_patch(Ellipse(position,width=width,height=height,angle=angle,fill=False,lw=0.5,alpha=0.6))

# Plotting Robot,

def plot_robot(x,y,theta,color='r'):
    radius = 0.2
    head_x = x + radius*np.cos(theta)
    head_y = y + radius*np.sin(theta)
    robot_circle = plt.Circle((x,y),radius,color=color,fill=False)
    ax = plt.gca()
    ax.plot([x,head_x],[y,head_y],color = 'b')
    ax.add_artist(robot_circle)
    plt.xlim(-3,12)
    plt.ylim(-3,12)
    
def plot_estimated_landmarks(mu,sigma,observedLandmarks,ids,color='g'):
    radius = 0.2
    ax = plt.gca()
    for i,(x,y) in enumerate(zip(mu[3::2],mu[4::2])):
        if(observedLandmarks[i] != 0):
            ax.plot(x,y,'bo')
            draw_ellipse((x,y),sigma[i*2+3:i*2+5,i*2+3:i*2+5],fill=False,alpha=0.9)
            if(i+1 in ids):
                ax.plot([mu[0],x],[mu[1],y],color = 'k',linewidth=0.2)
                
def plot_and_save_state(mu,sigma,observedLandmarks,landmarks,ids,i):
    plt.clf()
    plot_robot(mu[0],mu[1],mu[2])
    draw_ellipse((mu[0],mu[1]),sigma[0:2,0:2],alpha=0.5,fill=False)
    plot_estimated_landmarks(mu,sigma,observedLandmarks,ids)
    plot_landmarks(landmarks)
    plt.savefig('plots/ekf_{:>03}'.format(i+1))
