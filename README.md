# Lab course module: Image Analysis

This repository contains course material for the Image Analysis module of the Lab course of the Single Cell Facility of D-BSSE at ETH Zurich.

- The course is designed for Biotechnology Master students at D-BSSE who have varying levels of experience in image analysis
- we assume that students are mostly beginners in image analysis and programming
- The course is designed to be hands-on, with a focus on practical exercises and real-world applications of image analysis techniques
- It's a two day course
- In the microscopy part of the lab course (which students complete after this module), students acquire images which they will need to analyse (see homework.md for details)
- On the afternoon of the second day, students will work on a challenge (see challenge.md for details) that will require them to apply the skills they have learned in the course to a real-world image analysis problem
- the course aims to prepare students to autonomously complete the challenge and homework, and should give them a good first exposure to the basic and most important concepts in bioimage analysis
- data and exercises should include both
  1) a dataset and workflow which serves as a guiding motivation and example. This should be: images - preprocessing - segmentation - feature extraction - analysis and visualization
  2) small and fun exercises which allow students to explore and learn the concepts with some diversity and creativity
- practical part:
  - first, students will learn image basics and basic segmentation / feature extraction in Fiji
  - then, they will learn how to use Python for image analysis. Switching to Python is motivated by the need for flexible and reproducible workflows, as well as the need to batch process

- Teaching dynamics
  - Fiji part:
    - For each topic bundle:
      - concept explanation
      - interactive demonstration
      - exercises
        - format: markdown files with written out exercises and instructions, as well as example images
  - Python part:
    - For each topic bundle:
      - concept explanation
      - jupyter notebook to go through with students
      - exercises
        - format: jupyter notebooks with blanks for students to fill in, with hints and explanations

- images should be relatively small (not more than 512x512 pixels)
- solutions to the exercises are git ignored and not included in the repo, but can be provided to students upon request

## Computational environment

- Students clone the repo and install using pixi
- Data is included in the repo, which uses git-lfs

## Website

- There's a course website generated from the repo using jupyter-book

## Repository structure
- ./data: contains the example data used in the course
- ./notebooks: contains the Jupyter notebooks used in the course
- ./book: contains the jupyter-book source files