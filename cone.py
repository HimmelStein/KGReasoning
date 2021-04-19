import numpy as np
import util_cone as uc
SphereRadius = 10**8
THRESHOLD4ACTM = 0.1


class Cone:
    def __init__(self, vec, angle, beta):
        """
        vec and angle represent the center vector of a cone-shaped box
        beta is the offset vector in each dimension, each component of beta is in the range of [0, np.pi]
        """
        if angle == 0:
            self.vec = vec
            self.angle = uc.x2theta(vec)
            self.r = SphereRadius
            self.beta = beta
        elif vec == 0:
            self.vec = uc.theta2x(angle, SphereRadius)
            self.angle = uc.x2theta(self.vec)
            self.r = SphereRadius
            self.beta = beta
        elif vec != 0 and angle != 0:
            self.vec = vec
            self.angle = angle
            self.r = SphereRadius
            self.beta = beta

    def neg(self):
        return Cone(-self.vec, 0, np.pi - self.beta)

    def relation_with(self, cone):
        arccos = np.arccos(self.vec, cone.vec)
        beta_sum = self.beta + cone.beta
        if beta_sum > arccos and np.pi - arccos > beta_sum:
            return 1
        elif arccos > beta_sum: # disconnected
            return 0
        elif beta_sum > arccos and beta_sum >= np.pi - arccos:
            return 2
        else:
            return -1

    def intersect_with(self, cone, actM = False):
        arccos = np.arccos(self.vec, cone.vec)
        beta_sum = self.beta + cone.beta
        rel = self.relation_with(cone)
        if rel == 0:
            beta_inter = (beta_sum - arccos) / 2
            alpha = (cone.beta - beta_inter) / arccos
            angle_inter = alpha * self.angle + (1 - alpha) * cone.angle
            vec_inter = uc.theta2x(angle_inter, self.r)
            return Cone(vec_inter, angle_inter, 0)
        elif rel == 1:
            beta_inter = (beta_sum - arccos)/2
            alpha = (cone.beta - beta_inter)/arccos
            angle_inter = alpha * self.angle + (1-alpha)*cone.angle
            vec_inter = uc.theta2x(angle_inter, self.r)
            return Cone(vec_inter, angle_inter, beta_inter)
        elif rel == 2 and actM:
            return self.neg().union_with(cone.neg(), actM=actM).neg()
        else:
            return -1

    def union_with(self, cone, actM=False):
        arccos = np.arccos(self.vec, cone.vec)
        beta_sum = self.beta + cone.beta
        rel = self.relation_with(cone)
        if rel == 0 and not actM:
            beta_union = (beta_sum + arccos) / 2
            alpha = (beta_union + cone.beta) / arccos
            angle_union = alpha * self.angle + (1 - alpha) * cone.angle
            vec_union = uc.theta2x(angle_union, self.r)
            return Cone(vec_union, angle_union, beta_union)
        elif rel == 0 and actM:
            beta3 = (arccos - self.beta - cone.beta)/2
            alpha = (cone.beta + beta3)/arccos
            angle3 = alpha*uc.x2theta(self.vec) + (1-alpha)*uc.x2theta(cone.vec)
            cone3 = Cone(0, angle3, beta3)
            if np.abs(self.beta - beta3) > np.abs(cone.beta - beta3):
                if cone.threshold4swap(cone3):
                    uc.swap_cones(cone.vec, cone.angle, cone.beta, cone3.vec, cone3.angle, cone3.beta, r=SphereRadius)
                    return self.union_with(cone3, actM=False)
                else:
                    return self.union_with(cone, actM=False)
            else:
                if self.threshold4swap(cone3):
                    uc.swap_cones(self.vec, self.angle, self.beta, cone3.vec, cone3.angle, cone3.beta, r=SphereRadius)
                    return cone.union_with(cone3, actM=False)
                else:
                    return self.union_with(cone, actM=False)

        elif rel == 1:
            beta_union = (beta_sum + arccos) / 2
            alpha = (beta_union - cone.beta) / arccos
            angle_union = alpha * self.angle + (1 - alpha) * cone.angle
            vec_union = uc.theta2x(angle_union, self.r)
            return Cone(vec_union, angle_union, beta_union)
        elif rel == 2:
            return Cone(self.vec, self.angle, np.pi)
        else:
            return -1

    def threshold4swap(self, cone3):
        if self.beta/cone3.beta > THRESHOLD4ACTM:
            return True
        else:
            return False

    def contain(self, vec):
        if np.cos(self.vec, vec) > np.cos(self.beta):
            return True
        else:
            return False

