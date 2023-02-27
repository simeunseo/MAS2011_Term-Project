# MAS2011_Term-Project
Sogang Univ. Introduction to Visual Media Programming Term Project 1 - Chroma key

## About Project
We implemented digital matting also known as Chroma Keying technique, via color selection and masking. You can erase certain color parts of your video and add a new background.

## How to Use
#### 1. Prepare input video and background image
It will remove the background from your video and insert a new background. So The background in your video should have a even color and it must be a distinct color from the object.

#### 2. Run program
run in the terminal by a commend like :
```
 $ python chroma_key.py input_video.mp4  background.png output_video.mp4
```
#### 3. Pick color to remove
![image](https://user-images.githubusercontent.com/55528304/204782194-4e5c1121-95c4-48c2-ad26-db51bdf1b703.png)
You can see three window, 'panel_threshold', 'input_video' and 'result'. On the 'input_video' window, left-click the background part you want to remove.

#### 4. Adjust the threshold
In the 'panel_threshold' window, you can adjust the threshold that decides upper bound and lower bound of the range of color that you want to remove based on the color you just chose.
Find the right color and threshold that erases the background well.

## Project Team 
Eunseo Sim, Yunji Choi

