# This file is part of Tasks.
#
# Tasks is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Tasks is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Tasks.  If not, see <http://www.gnu.org/licenses/>.

from pybindgen import *
import sys

def import_sch_types(mod):
  mod.add_class('S_Object', foreign_cpp_namespace='sch', import_from_module='sch')
  mod.add_class('CD_Pair', foreign_cpp_namespace='sch', import_from_module='sch')



def import_rbd_types(mod):
  mod.add_class('Body', foreign_cpp_namespace='rbd', import_from_module='rbdyn')
  mod.add_class('Joint', foreign_cpp_namespace='rbd', import_from_module='rbdyn')
  mod.add_class('MultiBody', foreign_cpp_namespace='rbd', import_from_module='rbdyn')
  mod.add_class('MultiBodyConfig', foreign_cpp_namespace='rbd', import_from_module='rbdyn')
  mod.add_class('Jacobian', foreign_cpp_namespace='rbd', import_from_module='rbdyn')
  mod.add_class('CoMJacobianDummy', foreign_cpp_namespace='rbd', import_from_module='rbdyn')



def import_sva_types(mod):
  mod.add_class('MotionVecd', foreign_cpp_namespace='sva', import_from_module='spacevecalg')
  mod.add_class('ForceVecd', foreign_cpp_namespace='sva', import_from_module='spacevecalg')
  mod.add_class('RBInertiad', foreign_cpp_namespace='sva', import_from_module='spacevecalg')
  mod.add_class('ABInertiad', foreign_cpp_namespace='sva', import_from_module='spacevecalg')
  mod.add_class('PTransformd', foreign_cpp_namespace='sva', import_from_module='spacevecalg')



def import_eigen3_types(mod):
  mod.add_class('Vector3d', foreign_cpp_namespace='Eigen', import_from_module='eigen3')
  mod.add_class('Vector6d', foreign_cpp_namespace='Eigen', import_from_module='eigen3')

  mod.add_class('Matrix3d', foreign_cpp_namespace='Eigen', import_from_module='eigen3')
  mod.add_class('Matrix6d', foreign_cpp_namespace='Eigen', import_from_module='eigen3')

  mod.add_class('MatrixXd', foreign_cpp_namespace='Eigen', import_from_module='eigen3')
  mod.add_class('VectorXd', foreign_cpp_namespace='Eigen', import_from_module='eigen3')

  mod.add_class('Quaterniond', foreign_cpp_namespace='Eigen', import_from_module='eigen3')



def build_tasks(posTask, oriTask, positionTask, comTask, linVelTask, oriTrackTask):
  def add_std_func(cls):
    cls.add_method('update', None,
                   [param('const rbd::MultiBody&', 'mb'),
                    param('const rbd::MultiBodyConfig&', 'mbc')])

    cls.add_method('updateDot', None,
                   [param('const rbd::MultiBody&', 'mb'),
                    param('const rbd::MultiBodyConfig&', 'mbc')])

    cls.add_method('eval', retval('Eigen::VectorXd'), [], is_const=True)
    cls.add_method('jac', retval('Eigen::MatrixXd'), [], is_const=True)
    cls.add_method('jacDot', retval('Eigen::MatrixXd'), [], is_const=True)


  # PositionTask
  posTask.add_constructor([param('const rbd::MultiBody&', 'mb'),
                           param('int', 'bodyId'),
                           param('const Eigen::Vector3d&', 'pos'),
                           param('const Eigen::Vector3d&', 'bodyPoint',
                                 default_value='Eigen::Vector3d::Zero()')])

  posTask.add_method('position', None, [param('const Eigen::Vector3d&', 'pos')])
  posTask.add_method('position', retval('Eigen::Vector3d'), [], is_const=True)
  posTask.add_method('bodyPoint', None, [param('const Eigen::Vector3d&', 'point')])
  posTask.add_method('bodyPoint', retval('Eigen::Vector3d'), [], is_const=True)
  add_std_func(posTask)

  # OrientationTask
  oriTask.add_constructor([param('const rbd::MultiBody&', 'mb'),
                           param('int', 'bodyId'),
                           param('const Eigen::Quaterniond&', 'ori')])
  oriTask.add_constructor([param('const rbd::MultiBody&', 'mb'),
                           param('int', 'bodyId'),
                           param('const Eigen::Matrix3d&', 'ori')])

  oriTask.add_method('orientation', None, [param('const Eigen::Matrix3d&', 'ori')])
  oriTask.add_method('orientation', None, [param('const Eigen::Quaterniond&', 'ori')])
  oriTask.add_method('orientation', retval('Eigen::Matrix3d'), [], is_const=True)
  add_std_func(oriTask)

  # PostureTask
  postureTask.add_constructor([param('const rbd::MultiBody&', 'mb'),
                               param('std::vector<std::vector<double> >', 'q')])

  postureTask.add_method('posture', None,
                         [param('std::vector<std::vector<double> >', 'q')])
  postureTask.add_method('posture',
                         retval('std::vector<std::vector<double> >','q'), [],
                         is_const=True)
  add_std_func(postureTask)

  # CoMTask
  comTask.add_constructor([param('const rbd::MultiBody&', 'mb'),
                           param('const Eigen::Vector3d&', 'com')])
  comTask.add_constructor([param('const rbd::MultiBody&', 'mb'),
                           param('const Eigen::Vector3d&', 'com'),
                           param('std::vector<double>', 'weight')],
                           throw=[dom_ex])

  comTask.add_method('com', None, [param('const Eigen::Vector3d&', 'com')])
  comTask.add_method('com', retval('const Eigen::Vector3d&', 'com'), [],
                     is_const=True)
  add_std_func(comTask)

  # LinVelocityTask
  linVelTask.add_constructor([param('const rbd::MultiBody&', 'mb'),
                           param('int', 'bodyId'),
                           param('const Eigen::Vector3d&', 'pos'),
                           param('const Eigen::Vector3d&', 'bodyPoint',
                                 default_value='Eigen::Vector3d::Zero()')])

  linVelTask.add_method('velocity', None, [param('const Eigen::Vector3d&', 'pos')])
  linVelTask.add_method('velocity', retval('Eigen::Vector3d'), [], is_const=True)
  linVelTask.add_method('bodyPoint', None, [param('const Eigen::Vector3d&', 'point')])
  linVelTask.add_method('bodyPoint', retval('Eigen::Vector3d'), [], is_const=True)
  add_std_func(linVelTask)

  # OrientationTrackingTask
  oriTrackTask.add_constructor([param('const rbd::MultiBody&', 'mb'),
                                param('int', 'bodyId'),
                                param('const Eigen::Vector3d&', 'bodyPoint'),
                                param('const Eigen::Vector3d&', 'bodyAxis'),
                                param('const std::vector<int>&', 'trackingJointId'),
                                param('const Eigen::Vector3d&', 'trackedPoint')])

  oriTrackTask.add_method('trackedPoint', None, [param('const Eigen::Vector3d&', 'bPoint')])
  oriTrackTask.add_method('trackedPoint', retval('Eigen::Vector3d'), [], is_const=True)
  oriTrackTask.add_method('bodyPoint', None, [param('const Eigen::Vector3d&', 'tPoint')])
  oriTrackTask.add_method('bodyPoint', retval('Eigen::Vector3d'), [], is_const=True)
  oriTrackTask.add_method('bodyAxis', None, [param('const Eigen::Vector3d&', 'axis')])
  oriTrackTask.add_method('bodyAxis', retval('Eigen::Vector3d'), [], is_const=True)
  add_std_func(oriTrackTask)



def build_qp(tasks):
  qp = tasks.add_cpp_namespace('qp')

  sol = qp.add_class('QPSolver')
  solData = qp.add_class('SolverData')

  frictionCone = qp.add_struct('FrictionCone')
  unilateralContact = qp.add_struct('UnilateralContact')
  bilateralContact = qp.add_struct('BilateralContact')
  jointStiffness = qp.add_struct('JointStiffness')
  springJoint = qp.add_struct('SpringJoint')

  constr = qp.add_class('Constraint')
  ineqConstr = qp.add_class('Inequality')
  boundConstr = qp.add_class('Bound')

  task = qp.add_class('Task')
  hlTask = qp.add_class('HighLevelTask')

  spTask = qp.add_class('SetPointTask', parent=task)
  pidTask = qp.add_class('PIDTask', parent=task)
  toTask = qp.add_class('TargetObjectiveTask', parent=task)
  qTask = qp.add_class('QuadraticTask', parent=task)
  linWTask = qp.add_class('LinWeightTask', parent=task)

  posTask = qp.add_class('PositionTask', parent=hlTask)
  oriTask = qp.add_class('OrientationTask', parent=hlTask)
  postureTask = qp.add_class('PostureTask', parent=task)
  comTask = qp.add_class('CoMTask', parent=hlTask)
  contactTask = qp.add_class('ContactTask', parent=task)
  gripperTorqueTask = qp.add_class('GripperTorqueTask', parent=task)
  linVelTask = qp.add_class('LinVelocityTask', parent=hlTask)
  oriTrackTask = qp.add_class('OrientationTrackingTask', parent=hlTask)

  motionConstr = qp.add_class('MotionConstr', parent=[ineqConstr, boundConstr,
                                                      constr])
  motionPolyConstr = qp.add_class('MotionPolyConstr', parent=[ineqConstr, boundConstr,
                                                              constr])
  motionSpringConstr = qp.add_class('MotionSpringConstr', parent=[ineqConstr, boundConstr,
                                                                  constr])
  contactConstrCommon = qp.add_class('ContactConstrCommon')
  contactAccConstr = qp.add_class('ContactAccConstr', parent=[ineqConstr, constr, contactConstrCommon])
  contactSpeedConstr = qp.add_class('ContactSpeedConstr', parent=[ineqConstr, contactConstrCommon])

  selfCollisionConstr = qp.add_class('SelfCollisionConstr', parent=[ineqConstr, constr])
  seCollisionConstr = qp.add_class('StaticEnvCollisionConstr', parent=[ineqConstr, constr])
  comCollisionConstr = qp.add_class('CoMCollisionConstr', parent=[ineqConstr, constr])

  jointLimitsConstr = qp.add_class('JointLimitsConstr', parent=[boundConstr, constr])
  damperJointLimitsConstr = qp.add_class('DamperJointLimitsConstr', parent=[boundConstr, constr])

  gripperTorqueConstr = qp.add_class('GripperTorqueConstr', parent=[ineqConstr, constr])
  constantSpeedConstr = qp.add_class('ConstantSpeedConstr', parent=[ineqConstr, constr])


  constrName = ['MotionConstr', 'MotionPolyConstr', 'ContactAccConstr', 'ContactSpeedConstr',
                'SelfCollisionConstr', 'JointLimitsConstr', 'DamperJointLimitsConstr',
                'StaticEnvCollisionConstr', 'CoMCollisionConstr', 'MotionSpringConstr',
                'GripperTorqueConstr', 'ConstantSpeedConstr']
  ineqConstrName = ['MotionConstr', 'MotionPolyConstr', 'ContactAccConstr', 'ContactSpeedConstr',
                    'SelfCollisionConstr', 'StaticEnvCollisionConstr', 'CoMCollisionConstr',
                    'MotionSpringConstr', 'GripperTorqueConstr', 'ContactSpeedConstr']
  boundConstrName = ['MotionConstr', 'MotionPolyConstr', 'MotionSpringConstr','JointLimitsConstr', 'DamperJointLimitsConstr']
  taskName = ['QuadraticTask', 'SetPointTask', 'PIDTask', 'TargetObjectiveTask', 'LinWeightTask',
              'tasks::qp::PostureTask', 'tasks::qp::ContactTask',
              'tasks::qp::GripperTorqueTask']
  hlTaskName = ['PositionTask', 'OrientationTask', 'CoMTask', 'LinVelocityTask',
                'OrientationTrackingTask']
  constrList = [motionConstr, motionPolyConstr, contactAccConstr, contactSpeedConstr,
                selfCollisionConstr, seCollisionConstr, comCollisionConstr,
                jointLimitsConstr, damperJointLimitsConstr, motionSpringConstr,
                gripperTorqueConstr, constantSpeedConstr]


  # build list type
  tasks.add_container('std::vector<tasks::qp::FrictionCone>',
                      'tasks::qp::FrictionCone', 'vector')
  tasks.add_container('std::vector<tasks::qp::UnilateralContact>',
                      'tasks::qp::UnilateralContact', 'vector')
  tasks.add_container('std::vector<tasks::qp::BilateralContact>',
                      'tasks::qp::BilateralContact', 'vector')
  tasks.add_container('std::vector<tasks::qp::JointStiffness>',
                      'tasks::qp::JointStiffness', 'vector')
  tasks.add_container('std::vector<tasks::qp::SpringJoint>',
                      'tasks::qp::SpringJoint', 'vector')
  tasks.add_container('std::vector<Eigen::Vector3d>', 'Eigen::Vector3d', 'vector')
  tasks.add_container('std::vector<Eigen::Matrix3d>', 'Eigen::Matrix3d', 'vector')
  tasks.add_container('std::vector<Eigen::VectorXd>', 'Eigen::VectorXd', 'vector')
  tasks.add_container('std::vector<std::vector<Eigen::VectorXd> >', 'std::vector<Eigen::VectorXd>', 'vector')


  # QPSolver
  def add_std_solver_add_rm_nr(name, type):
    for t in type:
      ptr = '%s*' % t
      sol.add_method('add%s' % name, None,
                     [param(ptr, 'ptr', transfer_ownership=False)])
      sol.add_method('remove%s' % name, None,
                     [param(ptr, 'ptr', transfer_ownership=False)])

    sol.add_method('nr%ss' % name, retval('int'), [], is_const=True)

  sol.add_constructor([])
  sol.add_method('solve', retval('bool'),
                 [param('const rbd::MultiBody&', 'mb'),
                  param('const rbd::MultiBodyConfig&', 'mbc')])

  sol.add_method('updateConstrSize', None, [])

  sol.add_method('nrVars', None,
                 [param('const rbd::MultiBody&', 'mb'),
                  param('std::vector<tasks::qp::UnilateralContact>&', 'cont'),
                  param('std::vector<tasks::qp::BilateralContact>&', 'cont')])
  sol.add_method('nrVars', retval('int'), [], is_const=True)

  sol.add_method('updateTasksNrVars', None, [param('const rbd::MultiBody&', 'mb')],
                 is_const=True)
  sol.add_method('updateConstrsNrVars', None, [param('const rbd::MultiBody&', 'mb')],
                 is_const=True)
  sol.add_method('updateNrVars', None, [param('const rbd::MultiBody&', 'mb')],
                 is_const=True)

  add_std_solver_add_rm_nr('InequalityConstraint', ineqConstrName)
  add_std_solver_add_rm_nr('BoundConstraint', boundConstrName)
  add_std_solver_add_rm_nr('Constraint', constrName)
  add_std_solver_add_rm_nr('Task', taskName)
  sol.add_method('resetTasks', None, [])

  sol.add_method('result', retval('const Eigen::VectorXd&'), [], is_const=True)
  sol.add_method('alphaDVec', retval('Eigen::VectorXd'), [], is_const=True)
  sol.add_method('lambdaVec', retval('Eigen::VectorXd'), [], is_const=True)

  sol.add_method('contactLambdaPosition', retval('int'), [param('int', 'bodyId')], is_const=True)
  sol.add_method('data', retval('tasks::qp::SolverData'), [], is_const=True)


  # FrictionCone
  frictionCone.add_constructor([])
  frictionCone.add_constructor([param('Eigen::Matrix3d', 'frame'), param('int', 'nrGen'),
                                param('double', 'mu')])

  frictionCone.add_instance_attribute('generators', 'std::vector<Eigen::Vector3d>')

  # UnilateralContact
  unilateralContact.add_constructor([])
  unilateralContact.add_constructor([param('int', 'bodyId'),
                           param('const std::vector<Eigen::Vector3d>&', 'points'),
                           param('const Eigen::Matrix3d&', 'frame'),
                           param('int', 'nrGen'), param('double', 'mu')])

  unilateralContact.add_instance_attribute('bodyId', 'int')
  unilateralContact.add_instance_attribute('points', 'std::vector<Eigen::Vector3d>')
  unilateralContact.add_instance_attribute('cone', 'tasks::qp::FrictionCone')
  unilateralContact.add_method('sForce', retval('Eigen::Vector3d'),
                               [param('const Eigen::VectorXd&', 'lambda'),
                                param('int', 'point')],
                               throw=[dom_ex], custom_name='force')
  unilateralContact.add_method('sForce', retval('Eigen::Vector3d'),
                               [param('const Eigen::VectorXd&', 'lambda')],
                               throw=[dom_ex], custom_name='force')
  unilateralContact.add_method('sNrLambda', retval('int'), [param('int', 'point')],
                               is_const=True, throw=[dom_ex], custom_name='nrLambda')
  unilateralContact.add_method('nrLambda', retval('int'), [],
                               is_const=True, throw=[dom_ex])

  # BilateralContact
  bilateralContact.add_constructor([])
  bilateralContact.add_constructor([param('int', 'bodyId'),
                                    param('const Eigen::Vector3d&', 'center'),
                                    param('double', 'radius'),
                                    param('int', 'nrPoints'),
                                    param('const Eigen::Matrix3d&', 'frame'),
                                    param('int', 'nrGen'), param('double', 'mu')
                                   ])
  bilateralContact.add_constructor([param('int', 'bodyId'),
                                    param('const std::vector<Eigen::Vector3d>&', 'center'),
                                    param('const std::vector<Eigen::Matrix3d>&', 'frames'),
                                    param('int', 'nrGen'), param('double', 'mu')
                                   ])

  bilateralContact.add_instance_attribute('bodyId', 'int')
  bilateralContact.add_instance_attribute('points', 'std::vector<Eigen::Vector3d>')
  bilateralContact.add_instance_attribute('cones', 'std::vector<tasks::qp::FrictionCone>')
  bilateralContact.add_method('sForce', retval('Eigen::Vector3d'),
                              [param('const Eigen::VectorXd&', 'lambda'),
                               param('int', 'point')],
                              throw=[dom_ex], custom_name='force')
  bilateralContact.add_method('sForce', retval('Eigen::Vector3d'),
                              [param('const Eigen::VectorXd&', 'lambda')],
                              throw=[dom_ex], custom_name='force')
  bilateralContact.add_method('sNrLambda', retval('int'), [param('int', 'point')],
                              is_const=True, throw=[dom_ex], custom_name='nrLambda')
  bilateralContact.add_method('nrLambda', retval('int'), [],
                              is_const=True, throw=[dom_ex])

  # JointStiffness
  jointStiffness.add_constructor([])
  jointStiffness.add_constructor([param('int', 'jointId'),
                                  param('double', 'stiffness')])
  jointStiffness.add_instance_attribute('jointId', 'int')
  jointStiffness.add_instance_attribute('stiffness', 'std::vector<Eigen::Vector3d>')

  # SpringJoint
  springJoint.add_constructor([])
  springJoint.add_constructor([param('int', 'jointId'),
                               param('double', 'K'), param('double', 'C'),
                               param('double', 'O')])
  springJoint.add_instance_attribute('jointId', 'int')
  springJoint.add_instance_attribute('K', 'double')
  springJoint.add_instance_attribute('C', 'double')
  springJoint.add_instance_attribute('O', 'double')

  # Constraint
  constr.add_method('updateNrVars', None,
                    [param('const rbd::MultiBody&', 'mb'),
                     param('tasks::qp::SolverData', 'data')])

  constr.add_method('update', None,
                    [param('const rbd::MultiBody&', 'mb'),
                     param('const rbd::MultiBodyConfig&', 'mbc'),
                     param('const tasks::qp::SolverData&', 'data')])

  # InequalityConstraint
  ineqConstr.add_method('maxInEq', retval('int'), [])
  ineqConstr.add_method('nrInEq', retval('int'), [])
  ineqConstr.add_method('AInEq', retval('Eigen::MatrixXd'), [])
  ineqConstr.add_method('LowerInEq', retval('Eigen::MatrixXd'), [])
  ineqConstr.add_method('UpperInEq', retval('Eigen::MatrixXd'), [])

  # BoundConstraint
  boundConstr.add_method('beginVar', retval('int'), [])
  boundConstr.add_method('Lower', retval('Eigen::MatrixXd'), [])
  boundConstr.add_method('Upper', retval('Eigen::VectorXd'), [])

  # Task
  # task.add_constructor([param('double', 'weight')])

  task.add_method('weight', retval('double'), [], is_const=True)
  task.add_method('weight', None, [param('double', 'weight')])

  # task.add_method('update', None,
  #                 [param('const rbd::MultiBody&', 'mb'),
  #                  param('const rbd::MultiBodyConfig&', 'mbc')],
  #                 is_virtual=True, is_pure_virtual=True)

  # task.add_method('Q', retval('Eigen::MatrixXd'), [],
  #                 is_virtual=True, is_pure_virtual=True, is_const=True)
  # task.add_method('C', retval('Eigen::VectorXd'), [],
  #                 is_virtual=True, is_pure_virtual=True, is_const=True)

  # HighLevelTask
  hlTask.add_method('dim', retval('int'), [])

  hlTask.add_method('update', None,
                    [param('const rbd::MultiBody&', 'mb'),
                     param('const rbd::MultiBodyConfig&', 'mbc'),
                     param('const tasks::qp::SolverData&', 'data')])

  hlTask.add_method('jac', retval('Eigen::MatrixXd'), [])
  hlTask.add_method('eval', retval('Eigen::VectorXd'), [])
  hlTask.add_method('speed', retval('Eigen::VectorXd'), [])
  hlTask.add_method('normalAcc', retval('Eigen::VectorXd'), [])

  # SetPointTask
  def spConstructor(hlTaskName):
    for t in hlTaskName:
      name = 'tasks::qp::%s *' % t
      spTask.add_constructor([param('const MultiBody&', 'mb'),
                              param(name, 'hlTask',
                                    transfer_ownership=False),
                              param('double', 'stiffness'),
                              param('double', 'weight')])

      spTask.add_constructor([param('const MultiBody&', 'mb'),
                              param(name, 'hlTask',
                                    transfer_ownership=False),
                              param('double', 'stiffness'),
                              param('const Eigen::VectorXd&', 'dimWeight'),
                              param('double', 'weight')])

  spConstructor(hlTaskName)

  spTask.add_method('stiffness', retval('double'), [], is_const=True)
  spTask.add_method('stiffness', None, [param('double', 'weight')])

  spTask.add_method('dimWeight', retval('const Eigen::VectorXd&'), [], is_const=True)
  spTask.add_method('dimWeight', None, [param('const Eigen::VectorXd&', 'dim')])

  spTask.add_method('update', None,
                    [param('const rbd::MultiBody&', 'mb'),
                     param('const rbd::MultiBodyConfig&', 'mbc'),
                     param('const tasks::qp::SolverData&', 'data')])

  spTask.add_method('Q', retval('Eigen::MatrixXd'), [], is_const=True)
  spTask.add_method('C', retval('Eigen::VectorXd'), [], is_const=True)

  # TargetObjectiveTask
  def toConstructor(hlTaskName):
    for t in hlTaskName:
      name = 'tasks::qp::%s *' % t
      toTask.add_constructor([param('const MultiBody&', 'mb'),
                              param(name, 'hlTask',
                                    transfer_ownership=False),
                              param('double', 'timeStep'),
                              param('double', 'duration'),
                              param('const Eigen::VectorXd&', 'objDot'),
                              param('double', 'weight')])

      toTask.add_constructor([param('const MultiBody&', 'mb'),
                              param(name, 'hlTask',
                                    transfer_ownership=False),
                              param('double', 'timeStep'),
                              param('double', 'duration'),
                              param('const Eigen::VectorXd&', 'objDot'),
                              param('const Eigen::VectorXd&', 'dimWeight'),
                              param('double', 'weight')])

  toConstructor(hlTaskName)

  toTask.add_method('duration', retval('double'), [], is_const=True)
  toTask.add_method('duration', None, [param('double', 'd')])

  toTask.add_method('iter', retval('int'), [], is_const=True)
  toTask.add_method('iter', None, [param('int', 'i')])

  toTask.add_method('nrIter', retval('int'), [], is_const=True)
  toTask.add_method('nrIter', None, [param('int', 'i')])

  toTask.add_method('objDot', retval('const Eigen::VectorXd&'), [], is_const=True)
  toTask.add_method('objDot', None, [param('const Eigen::VectorXd&', 'obj')])

  toTask.add_method('dimWeight', retval('const Eigen::VectorXd&'), [], is_const=True)
  toTask.add_method('dimWeight', None, [param('const Eigen::VectorXd&', 'w')])

  toTask.add_method('phi', retval('const Eigen::VectorXd&'), [], is_const=True)
  toTask.add_method('psi', retval('const Eigen::VectorXd&'), [], is_const=True)

  toTask.add_method('update', None,
                    [param('const rbd::MultiBody&', 'mb'),
                     param('const rbd::MultiBodyConfig&', 'mbc'),
                     param('const tasks::qp::SolverData&', 'data')])

  toTask.add_method('Q', retval('Eigen::MatrixXd'), [], is_const=True)
  toTask.add_method('C', retval('Eigen::VectorXd'), [], is_const=True)

  # PIDTask
  def pidConstructor(hlTaskName):
    for t in hlTaskName:
      name = 'tasks::qp::%s *' % t
      pidTask.add_constructor([param('const MultiBody&', 'mb'),
                              param(name, 'hlTask',
                                    transfer_ownership=False),
                              param('double', 'P'),
                              param('double', 'I'),
                              param('double', 'D'),
                              param('double', 'weight')])

      pidTask.add_constructor([param('const MultiBody&', 'mb'),
                              param(name, 'hlTask',
                                    transfer_ownership=False),
                              param('double', 'P'),
                              param('double', 'I'),
                              param('double', 'D'),
                              param('const Eigen::VectorXd&', 'dimWeight'),
                              param('double', 'weight')])

  pidConstructor(hlTaskName)

  pidTask.add_method('P', retval('double'), [], is_const=True)
  pidTask.add_method('P', None, [param('double', 'weight')])
  pidTask.add_method('I', retval('double'), [], is_const=True)
  pidTask.add_method('I', None, [param('double', 'weight')])
  pidTask.add_method('D', retval('double'), [], is_const=True)
  pidTask.add_method('D', None, [param('double', 'weight')])

  pidTask.add_method('error', None, [param('const Eigen::VectorXd&', 'error')])
  pidTask.add_method('errorD', None, [param('const Eigen::VectorXd&', 'errorD')])
  pidTask.add_method('errorI', None, [param('const Eigen::VectorXd&', 'errorI')])

  pidTask.add_method('dimWeight', retval('const Eigen::VectorXd&'), [], is_const=True)
  pidTask.add_method('dimWeight', None, [param('const Eigen::VectorXd&', 'dim')])

  pidTask.add_method('update', None,
                    [param('const rbd::MultiBody&', 'mb'),
                     param('const rbd::MultiBodyConfig&', 'mbc'),
                     param('const tasks::qp::SolverData&', 'data')])

  pidTask.add_method('Q', retval('Eigen::MatrixXd'), [], is_const=True)
  pidTask.add_method('C', retval('Eigen::VectorXd'), [], is_const=True)

  # QuadraticTask
  def qConstructor(hlTaskName):
    for t in hlTaskName:
      name = 'tasks::qp::%s *' % t
      qTask.add_constructor([param('const MultiBody&', 'mb'),
                             param(name, 'hlTask',
                                   transfer_ownership=False),
                             param('double', 'weight')])

  qConstructor(hlTaskName)

  qTask.add_method('update', None,
                   [param('const rbd::MultiBody&', 'mb'),
                    param('const rbd::MultiBodyConfig&', 'mbc'),
                     param('const tasks::qp::SolverData&', 'data')])

  qTask.add_method('Q', retval('Eigen::MatrixXd'), [], is_const=True)
  qTask.add_method('C', retval('Eigen::VectorXd'), [], is_const=True)

  # LinWeightTask
  def linWConstructor(taskName):
    for t in taskName:
      name = '%s *' % t
      linWTask.add_constructor([param(name, 'task',
                                   transfer_ownership=False),
                                param('double', 'step'),
                                param('double', 'objWeight')])

  linWConstructor(taskName)

  linWTask.add_method('update', None,
                      [param('const rbd::MultiBody&', 'mb'),
                       param('const rbd::MultiBodyConfig&', 'mbc'),
                     param('const tasks::qp::SolverData&', 'data')])

  linWTask.add_method('Q', retval('Eigen::MatrixXd'), [], is_const=True)
  linWTask.add_method('C', retval('Eigen::VectorXd'), [], is_const=True)

  # PositionTask
  posTask.add_constructor([param('const rbd::MultiBody&', 'mb'),
                           param('int', 'bodyId'),
                           param('const Eigen::Vector3d&', 'pos'),
                           param('const Eigen::Vector3d&', 'bodyPoint',
                                 default_value='Eigen::Vector3d::Zero()')])

  posTask.add_method('position', None, [param('const Eigen::Vector3d&', 'pos')])
  posTask.add_method('position', retval('Eigen::Vector3d'), [], is_const=True)

  posTask.add_method('bodyPoint', None, [param('const Eigen::Vector3d&', 'point')])
  posTask.add_method('bodyPoint', retval('Eigen::Vector3d'), [], is_const=True)

  # OrientationTask
  oriTask.add_constructor([param('const rbd::MultiBody&', 'mb'),
                           param('int', 'bodyId'),
                           param('const Eigen::Quaterniond&', 'ori')])
  oriTask.add_constructor([param('const rbd::MultiBody&', 'mb'),
                           param('int', 'bodyId'),
                           param('const Eigen::Matrix3d&', 'ori')])

  oriTask.add_method('orientation', None, [param('const Eigen::Matrix3d&', 'ori')])
  oriTask.add_method('orientation', None, [param('const Eigen::Quaterniond&', 'ori')])
  oriTask.add_method('orientation', retval('Eigen::Matrix3d'), [], is_const=True)

  # PostureTask
  postureTask.add_constructor([param('const rbd::MultiBody&', 'mb'),
                               param('std::vector<std::vector<double> >', 'q'),
                               param('double', 'stiffness'),
                               param('double', 'weight')])


  postureTask.add_method('stiffness', retval('double'), [], is_const=True)
  postureTask.add_method('stiffness', None, [param('double', 'weight')])

  postureTask.add_method('posture', None,
                         [param('std::vector<std::vector<double> >', 'q')])
  postureTask.add_method('posture',
                         retval('std::vector<std::vector<double> >','q'), [],
                         is_const=True)

  postureTask.add_method('jointsStiffness', None,
                         [param('const rbd::MultiBody&', 'mb'),
                          param('std::vector<tasks::qp::JointStiffness>', 'js')])

  postureTask.add_method('update', None,
                    [param('const rbd::MultiBody&', 'mb'),
                     param('const rbd::MultiBodyConfig&', 'mbc'),
                     param('const tasks::qp::SolverData&', 'data')])
  postureTask.add_method('eval', retval('Eigen::VectorXd'), [])

  # CoMTask
  comTask.add_constructor([param('const rbd::MultiBody&', 'mb'),
                           param('const Eigen::Vector3d&', 'com')])
  comTask.add_constructor([param('const rbd::MultiBody&', 'mb'),
                           param('const Eigen::Vector3d&', 'com'),
                           param('std::vector<double>', 'weight')],
                           throw=[dom_ex])

  comTask.add_method('com', None, [param('const Eigen::Vector3d&', 'com')])
  comTask.add_method('com', retval('const Eigen::Vector3d&', 'com'), [],
                     is_const=True)

  # ContactTask
  contactTask.add_constructor([param('int', 'bodyId'),
                               param('double', 'stiffness'),
                               param('double', 'weight')])

  contactTask.add_method('error', None, [param('const Eigen::Vector3d&', 'error')])
  contactTask.add_method('errorD', None, [param('const Eigen::Vector3d&', 'errorD')])

  # GripperTorqueTask
  gripperTorqueTask.add_constructor([param('int', 'bodyId'),
                                     param('const Eigen::Vector3d&', 'origin'),
                                     param('const Eigen::Vector3d&', 'axis'),
                                     param('double', 'weight')])

  # LinVelocityTask
  linVelTask.add_constructor([param('const rbd::MultiBody&', 'mb'),
                              param('int', 'bodyId'),
                              param('const Eigen::Vector3d&', 'pos'),
                              param('const Eigen::Vector3d&', 'bodyPoint',
                                    default_value='Eigen::Vector3d::Zero()')])

  linVelTask.add_method('velocity', None, [param('const Eigen::Vector3d&', 'pos')])
  linVelTask.add_method('velocity', retval('Eigen::Vector3d'), [], is_const=True)

  linVelTask.add_method('bodyPoint', None, [param('const Eigen::Vector3d&', 'point')])
  linVelTask.add_method('bodyPoint', retval('Eigen::Vector3d'), [], is_const=True)

  # OrientationTrackingTask
  oriTrackTask.add_constructor([param('const rbd::MultiBody&', 'mb'),
                                param('int', 'bodyId'),
                                param('const Eigen::Vector3d&', 'bodyPoint'),
                                param('const Eigen::Vector3d&', 'bodyAxis'),
                                param('const std::vector<int>&', 'trackingJointId'),
                                param('const Eigen::Vector3d&', 'trackedPoint')])

  oriTrackTask.add_method('trackedPoint', None, [param('const Eigen::Vector3d&', 'bPoint')])
  oriTrackTask.add_method('trackedPoint', retval('Eigen::Vector3d'), [], is_const=True)
  oriTrackTask.add_method('bodyPoint', None, [param('const Eigen::Vector3d&', 'tPoint')])
  oriTrackTask.add_method('bodyPoint', retval('Eigen::Vector3d'), [], is_const=True)
  oriTrackTask.add_method('bodyAxis', None, [param('const Eigen::Vector3d&', 'axis')])
  oriTrackTask.add_method('bodyAxis', retval('Eigen::Vector3d'), [], is_const=True)

  # MotionConstr
  def addMotionDefault(motion):
    motion.add_method('computeTorque', None, [param('const Eigen::VectorXd&', 'alphaD'),
                                              param('const Eigen::VectorXd&', 'lambda')])
    motion.add_method('torque', retval('Eigen::VectorXd'), [], is_const=True)
    motion.add_method('torque', None, [param('const rbd::MultiBody&', 'mb'),
                                             param('rbd::MultiBodyConfig&', 'mbc')], is_const=True)

  motionConstr.add_constructor([param('const rbd::MultiBody', 'mb'),
                                param('std::vector<std::vector<double> >', 'lTorqueBounds'),
                                param('std::vector<std::vector<double> >', 'uTorqueBounds')])
  addMotionDefault(motionConstr)

  # MotionPolyConstr
  motionPolyConstr.add_constructor([param('const rbd::MultiBody', 'mb'),
                                    param('std::vector<std::vector<Eigen::VectorXd> >', 'lTorqueBounds'),
                                    param('std::vector<std::vector<Eigen::VectorXd> >', 'uTorqueBounds')])
  addMotionDefault(motionPolyConstr)

  # MotionSpringConstr
  motionSpringConstr.add_constructor([param('const rbd::MultiBody', 'mb'),
                                      param('std::vector<std::vector<double> >', 'lTorqueBounds'),
                                      param('std::vector<std::vector<double> >', 'uTorqueBounds'),
                                      param('const std::vector<tasks::qp::SpringJoint>&', 'springs')])
  addMotionDefault(motionSpringConstr)

  # ContactConstrCommon
  contactConstrCommon.add_method('addVirtualContact', retval('bool'), [param('int', 'bodyId')])
  contactConstrCommon.add_method('removeVirtualContact', retval('bool'), [param('int', 'bodyId')])
  contactConstrCommon.add_method('resetVirtualContacts', None, [])

  contactConstrCommon.add_method('addDofContact', retval('bool'), [param('int', 'bodyId', ),
                                                                   param('const Eigen::MatrixXd&', 'dof')])
  contactConstrCommon.add_method('removeDofContact', retval('bool'), [param('int', 'bodyId')])
  contactConstrCommon.add_method('resetDofContacts', None, [])

  # ContactAccConstr
  contactAccConstr.add_constructor([param('const rbd::MultiBody', 'mb')])
  contactAccConstr.add_method('updateDofContacts', None, [])

  # ContactSpeedConstr
  contactSpeedConstr.add_constructor([param('const rbd::MultiBody', 'mb'),
                                      param('double', 'timeStep')])
  contactSpeedConstr.add_method('updateDofContacts', None, [])

  # SelfCollisionConstr
  selfCollisionConstr.add_constructor([param('const rbd::MultiBody', 'mb'),
                                       param('double', 'step')])
  selfCollisionConstr.add_method('addCollision', None,
                                 [param('const rbd::MultiBody&', 'mb'),
                                  param('int', 'collId'),
                                  param('int', 'body1Id'),
                                  param('sch::S_Object*', 'body1', transfer_ownership=False),
                                  param('const sva::PTransformd&', 'body1T'),
                                  param('int', 'body2Id'),
                                  param('sch::S_Object*', 'body2', transfer_ownership=False),
                                  param('const sva::PTransformd&', 'body2T'),
                                  param('double', 'di'),
                                  param('double', 'ds'),
                                  param('double', 'damping'),
                                  param('double', 'dampingOff', default_value='0.')])

  selfCollisionConstr.add_method('rmCollision', retval('bool'),
                                 [param('int', 'collId')])
  selfCollisionConstr.add_method('nrCollisions', retval('int'),
                                 [], is_const=True)
  selfCollisionConstr.add_method('reset', None, []),

  # StaticEnvCollisionConstr
  seCollisionConstr.add_constructor([param('const rbd::MultiBody', 'mb'),
                                     param('double', 'step')])
  seCollisionConstr.add_method('addCollision', None,
                               [param('const rbd::MultiBody&', 'mb'),
                                param('int', 'collId'),
                                param('int', 'bodyId'),
                                param('sch::S_Object*', 'body', transfer_ownership=False),
                                param('const sva::PTransformd&', 'bodyT'),
                                param('int', 'envId'),
                                param('sch::S_Object*', 'env', transfer_ownership=False),
                                param('double', 'di'),
                                param('double', 'ds'),
                                param('double', 'damping'),
                                param('double', 'dampingOff', default_value='0.')])

  seCollisionConstr.add_method('rmCollision', retval('bool'), [param('int', 'collId')])
  seCollisionConstr.add_method('nrCollisions', retval('int'),
                               [], is_const=True)
  seCollisionConstr.add_method('reset', None, []),

  #CoMCollisionConstr
  comCollisionConstr.add_constructor([param('const rbd::MultiBody', 'mb'),
                                      param('double', 'step')])
  comCollisionConstr.add_method('addCollision', None,
                               [param('const rbd::MultiBody&', 'mb'),
                                param('int', 'collId'),
                                param('sch::S_Object*', 'env', transfer_ownership=False),
                                param('double', 'di'),
                                param('double', 'ds'),
                                param('double', 'damping'),
                                param('double', 'dampingOff', default_value='0.')])

  comCollisionConstr.add_method('rmCollision', retval('bool'), [param('int', 'collId')])
  comCollisionConstr.add_method('nrCollisions', retval('int'),
                               [], is_const=True)
  comCollisionConstr.add_method('reset', None, []),


  # JointLimitsConstr
  jointLimitsConstr.add_constructor([param('const rbd::MultiBody&', 'mb'),
                                    param('std::vector<std::vector<double> >', 'lbound'),
                                    param('std::vector<std::vector<double> >', 'ubound'),
                                    param('double', 'step')])

  # DamperJointLimitsConstr
  damperJointLimitsConstr.add_constructor([param('const rbd::MultiBody&', 'mb'),
                                    param('const std::vector<std::vector<double> >&', 'lBound'),
                                    param('const std::vector<std::vector<double> >&', 'uBound'),
                                    param('std::vector<std::vector<double> >', 'lVel'),
                                    param('std::vector<std::vector<double> >', 'uVel'),
                                    param('double', 'interPercent'), param('double', 'securityPercent'),
                                    param('double', 'damperOffset'), param('double', 'step')])

  # GripperTorqueConstr
  gripperTorqueConstr.add_constructor([])
  gripperTorqueConstr.add_method('addGripper', None,
                                 [param('int', 'bodyId'), param('double', 'torqueLimit'),
                                  param('const Eigen::Vector3d&', 'origin'),
                                  param('const Eigen::Vector3d&', 'axis')]);
  gripperTorqueConstr.add_method('rmGripper', retval('bool'),
                                 [param('int', 'bodyId')])
  gripperTorqueConstr.add_method('reset', None, [])

  # ConstantSpeedConstr
  constantSpeedConstr.add_constructor([param('const rbd::MultiBody&', 'mb'),
                                       param('double', 'timeStep')])
  constantSpeedConstr.add_method('addConstantSpeed', None,
                                 [param('const rbd::MultiBody&', 'mb'), param('int', 'bodyId'),
                                  param('const Eigen::Vector3d&', 'bodyPoint'),
                                  param('const Eigen::MatrixXd&', 'dof'),
                                  param('const Eigen::VectorXd&', 'speed')])
  constantSpeedConstr.add_method('removeConstantSpeed', retval('bool'),
                                 [param('int', 'bodyId')])
  constantSpeedConstr.add_method('resetConstantSpeed', None, [])
  constantSpeedConstr.add_method('nrConstantSpeed', retval('int'), [])


  def add_add_remove_solver(constr):
    for c in constr:
      c.add_method('addToSolver', None, [param('tasks::qp::QPSolver&', 'solver')])
      c.add_method('removeFromSolver', None, [param('tasks::qp::QPSolver&',  'solver')])
  add_add_remove_solver(constrList)




if __name__ == '__main__':
  if len(sys.argv) < 2:
    sys.exit(1)

  tasks = Module('_tasks', cpp_namespace='::tasks')
  tasks.add_include('<Tasks.h>')
  tasks.add_include('<QPSolver.h>')
  tasks.add_include('<QPTasks.h>')
  tasks.add_include('<QPConstr.h>')
  tasks.add_include('<QPMotionConstr.h>')

  tasks.add_include('<RBDyn/MultiBodyConfig.h>')

  tasks.add_include('<sch/S_Object/S_Object.h>')
  tasks.add_include('<sch/S_Object/S_Sphere.h>')
  tasks.add_include('<sch/CD/CD_Pair.h>')

  dom_ex = tasks.add_exception('std::domain_error', foreign_cpp_namespace=' ',
                               message_rvalue='%(EXC)s.what()')
  out_ex = tasks.add_exception('std::out_of_range', foreign_cpp_namespace=' ',
                               message_rvalue='%(EXC)s.what()')

  # import Eigen3, sva and rbd types
  import_eigen3_types(tasks)
  import_sva_types(tasks)
  import_rbd_types(tasks)
  import_sch_types(tasks)

  posTask = tasks.add_class('PositionTask')
  oriTask = tasks.add_class('OrientationTask')
  postureTask = tasks.add_class('PostureTask')
  comTask = tasks.add_class('CoMTask')
  linVelTask = tasks.add_class('LinVelocityTask')
  oriTrackTask = tasks.add_class('OrientationTrackingTask')

  # build list type
  tasks.add_container('std::vector<int>', 'int', 'vector')
  tasks.add_container('std::vector<double>', 'double', 'vector')
  tasks.add_container('std::vector<std::vector<double> >', 'std::vector<double>', 'vector')

  build_tasks(posTask, oriTask, postureTask, comTask, linVelTask, oriTrackTask)

  # qp
  build_qp(tasks)




  with open(sys.argv[1], 'w') as f:
    tasks.generate(f)

