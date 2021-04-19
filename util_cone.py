import numpy as np

MINI_ANGLE = 10e-7

def x2theta(vec):
    def one_vec_to_theta(xrow):
        l = np.linalg.norm(xrow)
        one_angle = [np.arccos(xrow[0] / l)]
        rsin_theta, j = l, 1
        while j < dim-1:
            if one_angle[j - 1] == 0:
                one_angle[j - 1] = MINI_ANGLE
            rsin_theta0=rsin_theta
            rsin_theta *= np.sin(one_angle[j - 1])
            if rsin_theta == 0:
                print("rsin_theta0",rsin_theta0, one_angle[j - 1], np.sin(one_angle[j - 1]))
            cos_theta = xrow[j] / rsin_theta
            if cos_theta > 1: cos_theta = 1
            if cos_theta < -1: cos_theta = -1
            one_angle.append(np.arccos(cos_theta))
            j += 1
        return np.array(one_angle)
    vec = vec.cpu().detach().numpy()
    row = vec[0]
    dim = len(row)
    theta = np.array([one_vec_to_theta(one_row) for one_row in vec])
    return theta


def theta2x(angle, r=1):
    def one_theta2x(one_angle, l=1):
        vec = [l*np.cos(one_angle[0])]
        rsin, j = 1, 1
        while j < angle_dim:
            if one_angle[j - 1] == 0:
                one_angle[j - 1] == MINI_ANGLE
            rsin *= np.sin(one_angle[j - 1])
            vec.append(l*rsin*np.cos(one_angle[j]))
            j += 1
        vec.append(l*rsin * np.sin(one_angle[-1]))
        return np.array(vec)

    angle = angle.cpu().detach().numpy()
    first_angle = angle[0]
    angle_dim = len(first_angle)
    theta = np.array([one_theta2x(an_angle, l=r) for an_angle in angle])
    return theta


def swap_cones(vec2, beta2, angle2, vec3, angle3, beta3, r=1, data=None):
    new_data = []
    for entity, vecx in data:
        if np.cos(vecx, vec2) > np.cos(beta2):
            new_vecx = theta2x( beta3*(x2theta(vecx)-angle2)/beta2 + angle3, r)
        elif np.cos(vecx, vec3) > np.cos(beta3):
            new_vecx = theta2x( beta2*(x2theta(vec3) - angle3)/beta3 + angle2, r)
        else:
            new_vecx = vecx
        new_data[entity] = new_vecx
    # save data











