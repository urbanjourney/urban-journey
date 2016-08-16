"""Package that contains a number of functions to create transformation 
matrices between different reference frames."""

import numpy as np
import math
from numpy import ndarray as numpy_array

def TCI(t, omega_t = 7.2921235169904e-5):
    """Transformation Matrix from :ref:`sec:F-I` to :ref:`sec:F-C`.
    
    Parameters
    ----------
    t : float
        Time (s) to determine the rotation of the Earth.
    omega_t : float, optional
        Earth's rotational rate (rad/s).
    
    Returns
    -------
    TCI : numpy_array
        Transformation matrix from Inertial to ECEF frame.
    """
    
    return np.array([[math.cos(omega_t*t),  math.sin(omega_t*t), 0],
                     [-math.sin(omega_t*t), math.cos(omega_t*t), 0],
                     [0,                    0,                   1]])
    
def TIC(t, omega_t = 7.2921235169904e-5):
    """Transformation Matrix from :ref:`sec:F-C` to  :ref:`sec:F-I`.
    
    Parameters
    ----------
    t : float 
        Time (s) to determine the rotation of the Earth.
    omega_t : float, optional
        Earth's rotational rate (rad/s).
        
    Returns
    -------
    TIC : numpy_array
        Transformation matrix from ECEF to Inertial frame.
    """
    
    return TCI(t,omega_t).transpose()

def Tab(alpha, beta):
    """Transformation Matrix from :ref:`sec:F-b` to :ref:`sec:F-a`.
    
    Parameters
    ----------
    alpha : float
        Aerodynamic angle of attack (radians).
    beta : float
        Aerodynamic angle of side-slip (radians).
        
    Returns
    -------
    Tab : numpy_array 
        Transformation matrix from body to aerodynamic frame.
    """
    
    sang = np.sin([alpha, beta])
    cang = np.cos([alpha, beta])
    
    return np.array([[cang[1]*cang[0], sang[1], cang[1]*sang[0]],
                     [-sang[1]*cang[0], cang[1], -sang[1]*sang[0]],
                     [-sang[0], 0, cang[0]]])
    
def Tba(alpha, beta):
    """Transformation Matrix from :ref:`sec:F-a` to :ref:`sec:F-b`.
    
    Parameters
    ----------
    alpha : float
        Aerodynamic angle of attack (radians).
    beta : float
        Aerodynamic angle of side-slip (radians).
        
    Returns
    -------
    Tba : numpy_array
        Transformation matrix from aerodynamic to body frame.
    """
    
    return Tab(alpha,beta).transpose()

def TEC(tau, delta):
    """Transformation from :ref:`sec:F-C` to the :ref:`sec:F-E`.
    
    Parameters
    ----------
    tau : float
        Longitude (radians) from the Greenwich meridian (tau is positive if 
        the vehicle position is east of the Greenwich meridian).
    delta : float
        Latitude (radians) from the equator (delta is positive if the vehicle
        location is on the northern hemisphere).
    
    Returns
    -------
    TEC : numpy_array
        Transformation matrix from ECEF to Vehicle carried normal frame.
    """
    
    sang = np.sin([tau, delta])
    cang = np.cos([tau, delta])
    
    return np.array([[-sang[1]*cang[0], -sang[1]*sang[0], cang[1]],
                     [-sang[0], cang[0], 0],
                     [-cang[1]*cang[0], -cang[1]*sang[0], -sang[1]]])
    
def TCE(tau, delta):
    """Transformation from :ref:`sec:F-E` to the :ref:`sec:F-C`.
    
    Parameters
    ----------
    tau : float
        Longitude (radians) from the Greenwich meridian (tau is positive if 
        the vehicle position is east of the Greenwich meridian).
    delta : float
        Latitude (radians) from the equator (delta is positive if the vehicle
        location is on the northern hemisphere).
        
    Returns
    -------
    TCE : numpy_array
        Transformation matrix from Vehicle carried normal frame to ECEF.
    """
    
    return TEC(tau, delta).transpose()

def TbE(psi, theta, phi):
    """Transformation from :ref:`sec:F-E` to the :ref:`sec:F-b`.
    
    Parameters
    ----------
    psi : float 
        Yaw angle about the Z_E-axis (radians).
    theta : float
        Pitch angle about the Y_E-axis (radians).
    phi : float
        Roll angle about the X_E-axis (radians).
    
    Returns
    -------
    TbE : numpy_array
        Transformation matrix from ECEF to body frame.
    """
    
    sang = np.sin([psi, theta, phi])
    cang = np.cos([psi, theta, phi])
    
    return np.array([[cang[1]*cang[0], cang[1]*sang[0], -sang[1]],
                     [sang[2]*sang[1]*cang[0]-cang[2]*sang[0], sang[2]*sang[1]*sang[0]+cang[2]*cang[0], sang[2]*cang[1]],
                     [cang[2]*sang[1]*cang[0]+sang[2]*sang[0], cang[2]*sang[1]*sang[0]-sang[2]*cang[0], cang[2]*cang[1]]])

def TEb(psi, theta, phi):
    """Transformation from the :ref:`sec:F-b` to :ref:`sec:F-E`.
    
    Parameters
    ----------
    psi : float 
        Yaw angle about the Z_E-axis (radians).
    theta : float
        Pitch angle about the Y_E-axis (radians).
    phi : float
        Roll angle about the X_E-axis (radians).
    
    Returns
    -------
    TEb : numpy_array
        Transformation matrix from body to ECEF frame.
    """
    
    return TbE(psi, theta, phi).transpose()

def TaE(chi, gamma, mu):
    """Transformation from the :ref:`sec:F-E` to the :ref:`sec:F-a`.
    
    Parameters
    ----------
    chi : float
        Aerodynamic heading angle about the Z_E-axis (radians).
    gamma : float
        Aerodynamic flight-path angle about the Y_E-axis (radians).
    mu : float 
        Aerodynamic bank angle about the X_a-axis (radians).
    
    Returns
    -------
    TaE : numpy_array
        Transformation matrix from Vehicle carried normal to aerodynamic frame. 
    """
    
    sang = np.sin([chi, gamma, mu])
    cang = np.cos([chi, gamma, mu])
    
    return np.array([[cang[1]*cang[0], cang[1]*sang[0], -sang[1]],
                     [-sang[2]*sang[1]*cang[0]-cang[2]*sang[0], -sang[2]*sang[1]*sang[0]+cang[2]*cang[0], -sang[2]*cang[1]],
                     [cang[2]*sang[1]*cang[0]-sang[2]*sang[0], cang[2]*sang[1]*sang[0]+sang[2]*cang[0], cang[2]*cang[1]]])

def TEa(chi, gamma, mu):
    """Transformation from the :ref:`sec:F-a` to the :ref:`sec:F-E`.
    
    Parameters
    ----------
    chi : float
        Aerodynamic heading angle about the Z_E-axis (radians).
    gamma : float
        Aerodynamic flight-path angle about the Y_E-axis (radians).
    mu : float 
        Aerodynamic bank angle about the X_a-axis (radians).
        
    Returns
    -------
    TEa : numpy_array
        Transformation matrix from aerodynamic to Vehicle carried normal frame.
    """
    
    return TaE(chi, gamma, mu).transpose()