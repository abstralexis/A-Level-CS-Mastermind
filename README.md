# A-Level-CS-Mastermind
This is a CS project where we make the Mastermind board game. I am going to try different languages and approaches.

## What language will I use?

I have many ideas as to what language I could use for this project, however I feel like they have many different downsides. A language like C/C++ needs low level bindings and such for OpenGl/GLFW, Java is very verbose and I am unfamiliar with LWJGL, Python has very limited scope and speed, and the Rust ecosystem is not fully mature yet for something like making a game. I fear that I will have to make a whole engine for this project.

## HTML/CSS/JavaScript Attempt

First, I tried doing small little graphical demos and such with HTML, CSS, and JavaScript. I am a big fan of the style one is able to achieve with CSS, with the `darkslateblue` to `black` gradients etc., and I do not mind how HTML is formatted. However, I really dislike JavaScript's syntax, and the lack of easy error detection. It is also not very straightforward to make structs/classes, and JavaScript is also unsafe. I want to make a program that is robust, easy to read, write, and modify, as well as good looking and fun on the user's end. Hence, I am ruling out a Web App/JavaScript as an option for this project.

## Rust w/ Bevy Attempt

I tried to start some stuff with Bevy, a rust library for making small graphical games. Bevy itself refused to compile, so I could not go further with it. I also find the way it structures programs to be very confusing.

## Python w/ Pygame Attempt

I decided to just fall back onto Pygame as my programming option. Doing a bit each day, it did not take long to get a fairly good looking version of Mastermind working. I am really proud of this game. One issue at the moment is the code is somewhat all over the place and uncommented, so I need to clean it up at some point. In addition, because of the way Pygame handles inputs per frame, I had to set the framerate really low. That doesn't matter at all for user experience except for the fact that some inputs are dropped in exchange for inputs that do not repeat if the framerate is too high.

## Documenting what I have done with GitHub Pages

After I got the Pygame version of Mastermind up and running, I decided to start making a page on GitHub pages to format documentation and other things about the process of making this program in a nicer way. I plan to include a QR code to that site on the poster we have to make of our program, but first I need to make it look better and clean up my code more. I am fairly proud of this project as it is the closest thing to a real production game that I have made myself, and it wasn't too complicated. I feel like from here I need to start stretching myself more with lower level theory and languages, and more complex projects that may involve a longer time commitment for learning things like maths of other theory that can apply.
