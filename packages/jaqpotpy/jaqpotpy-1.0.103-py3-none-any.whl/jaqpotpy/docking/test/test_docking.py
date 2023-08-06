"""
Tests for Docking
"""
import os
import platform
import unittest
import pytest
import logging
import numpy as np
import jaqpotpy as jp
from jaqpotpy.descriptors import ComplexFeaturizer
from jaqpotpy.models import Model
from jaqpotpy.docking.pose_generation import PoseGenerator

IS_WINDOWS = platform.system() == 'Windows'


class TestDocking(unittest.TestCase):
  """
  Does sanity checks on pose generation.
  """

  def setUp(self):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # self.protein_file = os.path.join(current_dir, "1jld_protein.pdb")
    # self.protein_file = os.path.join(current_dir, "7zb6.pdb")
    self.protein_file = os.path.join(current_dir, "2_a.pdb")
    self.ligand_file = os.path.join(current_dir, "mulno.sdf")
    # self.ligand_file = os.path.join(current_dir, "1jld_ligand.sdf")

    # self.protein_file = os.path.join(current_dir, "1a9m_pocket.pdb")
    # self.ligand_file = os.path.join(current_dir, "1a9m_ligand.sdf")
    # self.ligand_file = os.path.join(current_dir, "ZINC000787318646.sdf")

  @pytest.mark.slow
  def test_docker_init(self):
    """Test that Docker can be initialized."""
    vpg = jp.docking.VinaPoseGenerator()
    jp.docking.Docker(vpg)

  # @unittest.skip("skipping automated test")
  @unittest.skipIf(IS_WINDOWS, "vina is not supported in windows")
  @pytest.mark.slow
  def test_docker_dock(self):
    """Test that Docker can dock."""
    # We provide no scoring model so the docker won't score
    vpg = jp.docking.VinaPoseGenerator(calc_charges=False, add_hydrogens=False)
    docker = jp.docking.Docker(vpg)
    docked_outputs = docker.dock((self.protein_file, self.ligand_file),
                                 exhaustiveness=12,
                                 num_modes=4,
                                 out_dir="./tmp",
                                 use_pose_generator_scores=True)

    print(docked_outputs)
    print(list(docked_outputs))
    # Check only one output since num_modes==1
    assert len(list(docked_outputs)) == 4

  @unittest.skip("skipping automated test")
  @unittest.skipIf(IS_WINDOWS, "vina is not supported in windows")
  @pytest.mark.slow
  def test_docker_pose_generator_scores(self):
    """Test that Docker can get scores from pose_generator."""
    # We provide no scoring model so the docker won't score
    vpg = jp.docking.VinaPoseGenerator()
    docker = jp.docking.Docker(vpg)
    docked_outputs = docker.dock((self.protein_file, self.ligand_file),
                                 exhaustiveness=4,
                                 num_modes=4,
                                 out_dir="./tmp",
                                 use_pose_generator_scores=True)

    # Check only one output since num_modes==1
    docked_outputs = list(docked_outputs)
    print(docked_outputs)
    print(len(docked_outputs))
    print(len(docked_outputs[0]))
    assert len(docked_outputs) == 4
    assert len(docked_outputs[0]) == 2

  @unittest.skip("skipping automated test")
  @unittest.skipIf(IS_WINDOWS, "vina is not supported in windows")
  @pytest.mark.slow
  def test_docker_pose_generator_scores_on_pocket(self):
    """Test that Docker can get scores from pose_generator."""
    # We provide no scoring model so the docker won't score
    vpg = jp.docking.VinaPoseGenerator()
    docker = jp.docking.Docker(vpg)
    docked_outputs = docker.dock((self.protein_file, self.ligand_file),
                                 exhaustiveness=40,
                                 num_modes=4,
                                 out_dir="./tmp",
                                 use_pose_generator_scores=True)

    # Check only one output since num_modes==1
    docked_outputs = list(docked_outputs)
    print(docked_outputs)
    assert len(docked_outputs) == 1
    assert len(docked_outputs[0]) == 2

  @unittest.skip("skipping automated test")
  @unittest.skipIf(IS_WINDOWS, "vina is not supported in windows")
  @pytest.mark.slow
  def test_docker_specified_pocket(self):
    """Test that Docker can dock into spec. pocket."""
    # Let's turn on logging since this test will run for a while
    logging.basicConfig(level=logging.INFO)
    vpg = jp.docking.VinaPoseGenerator()
    docker = jp.docking.Docker(vpg)
    docked_outputs = docker.dock((self.protein_file, self.ligand_file),
                                 centroid=(10, 10, 10),
                                 box_dims=(10, 10, 10),
                                 exhaustiveness=1,
                                 num_modes=1,
                                 out_dir="./tmp")

    # Check returned files exist
    assert len(list(docked_outputs)) == 1

  @unittest.skip("skipping automated test")
  @unittest.skipIf(IS_WINDOWS, "vina is not supported in windows")
  @pytest.mark.slow
  def test_pocket_docker_dock(self):
    """Test that Docker can find pockets and dock dock."""
    # Let's turn on logging since this test will run for a while
    logging.basicConfig(level=logging.INFO)
    pocket_finder = jp.docking.ConvexHullPocketFinder()
    vpg = jp.docking.VinaPoseGenerator(pocket_finder=pocket_finder)
    docker = jp.docking.Docker(vpg)
    docked_outputs = docker.dock((self.protein_file, self.ligand_file),
                                 exhaustiveness=1,
                                 num_modes=1,
                                 num_pockets=1,
                                 out_dir="./tmp")

    # Check returned files exist
    assert len(list(docked_outputs)) == 1

  @pytest.mark.slow
  def test_scoring_model_and_featurizer(self):
    """Test that scoring model and featurizer are invoked correctly."""

    class DummyFeaturizer(ComplexFeaturizer):

      def featurize(self, complexes, *args, **kwargs):
        return np.zeros((len(complexes), 5))

    class DummyModel(Model):

      def predict(self, dataset, *args, **kwargs):
        return np.zeros(len(dataset))

    class DummyPoseGenerator(PoseGenerator):

      def generate_poses(self, *args, **kwargs):
        return [None]

    featurizer = DummyFeaturizer()
    scoring_model = DummyModel()
    pose_generator = DummyPoseGenerator()
    docker = jp.docking.Docker(pose_generator, featurizer, scoring_model)
    outputs = docker.dock(None)
    assert list(outputs) == [(None, np.array([0.]))]