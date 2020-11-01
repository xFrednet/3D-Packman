# Report: 3D Terrain - rendering smooth was yesterday

## Table of Contents
* 1 [Introduction](#1-introduction)
    * 1.1 [Inspiration and backstory](#11-Inspiration-and-backstory)
    * 1.2 [Goal](#12-Goal)

## 1 Introduction
This report is part of the assignment 5. It covers the 3D terrain rendering and especially the interesting parts of this project as well as a description how this was developed.

You can skip to the interesting parts using the [table of contents](#Table-of-Contents) or read the entire report. It should be an easy and hopefully fun read :).

### 1.1 Inspiration and backstory
I'm really interested in game development in general. This is what got me into this degree. I used to match [_ThinMatrix_](https://www.youtube.com/user/ThinMatrix/) and [_The Cherno_](https://www.youtube.com/c/TheChernoProject/featured) both are YouTubers that focus on game development from scratch.

I even tried to develop my own game engine but I gave up after several month, when I saw the source code of the _Unreal Engine_. Anyways my focus shifted from game engine development to 2D game development and low level stuff. It was at this time that ThinMatrix started to develop a low poly game. And I started to love the aesthetics of low poly games and objects. It's crazy how models with very little detail can look better than some fancy models.

I always played with the idea of coming back to 3D game development to create a low poly game. This and the compiler course was actually one of the main reasons why I choose _Reykjavik University_ for my semester abroad. I couldn't be happier with my choice. I've come to a point where I can fluently interact with OpenGL. My focus will be on other projects after this semester but I hope that there will be time to continue working on something like this. Vulkan and [RLSL](https://maikklein.github.io/shading-language-part1/) (Rust Like Shading Language) are two topics that I would like to look into if there is the time :)

### 1.2 Goal
At the start of this project I defined the following goals:
1. Create a low poly terrain with water animation and lighting support
2. Use a geometry shader somewhere in the project
3. Create a performance friendly particle system (Maybe like the one used in old [LEGO Star Wars](https://www.youtube.com/watch?v=JK1aV_mzH3A) games)
4. Have a better and reusable project structure
5. Calculate as much as possible in the shaders them self (This one was added during development)

Most of these goals are self explanatory. However, I want to add some notes to 2. and 4.:
* My goal is always to learn, this is the reason why I chose this course. I believe that I'm fairly fluent with vertex and fragment shaders but I've never tried to work this geometry shaders. I believe that these shaders add so many abilities that I really wanted to work with it
* I knew that I wouldn't be able to create an entire game with learning a new shader type. So, I set my self the goal to create an architecture that is good enough that I can continue working with it after the end of this course.

Okay, that is enough introduction for now. Let's get into some fun and technical stuff

## 2 Geometry

## 3 Implementation

### 3.1 Terrain 

### 3.2 Water

### 3.3 Particles 

## 4. Final thoughts