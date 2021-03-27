using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
/*
 * Author = Petr Bobčík (xbobci02)
 * 
 */
public class OnMouseDown : MonoBehaviour
{
    public GameObject myImg, UIManagerObj;
    Image myImageComponent;
    private UIManager uiScript;
    public Sprite upArrow, rightArrow, leftArrow, downArrow, robot, goal, obstacle, wall, mine, wall_v; //Drag your first sprite here in inspector.
    public Text label;
    public Toggle toggle;
    public bool down;

    void Start() //Lets start by getting a reference to our image component.
    {
        myImageComponent = myImg.GetComponent<Image>(); //Our image component is the one attached to this gameObject.
        uiScript = UIManagerObj.GetComponent<UIManager>();
    }

    //Setting an image(arrows, robot, goal, etc.) depending on what the mouse cursor is pointing at
    public void WhoAmI()
    {
        if (label.text == "Up Arrow")
        {
            myImageComponent.sprite = upArrow;
        } else if (label.text == "Right Arrow")
        {
            myImageComponent.sprite = rightArrow;
        }
        else if (label.text == "Left Arrow")
        {
            myImageComponent.sprite = leftArrow;
        }
        else if (label.text == "Down Arrow")
        {
            myImageComponent.sprite = downArrow;
        }
        else if (label.text == "Robot")
        {
            myImageComponent.sprite = robot;
        }
        else if (label.text == "Goal")
        {
            myImageComponent.sprite = goal;
        }
        else if (label.text == "Mine")
        {
            myImageComponent.sprite = obstacle;
        }
        else if (label.text == "Wall Horizontal")
        {
            myImageComponent.sprite = wall;
        }
        else if (label.text == "Wall Vertical")
        {
            myImageComponent.sprite = wall_v;
        }
    }
    
    //Creating an object(arrows, robot, goal, etc.) depending on what is clicked on
    public void createThing()
    {
        if (label.text == "Up Arrow")
        {
            uiScript.createArrow("up");
        }
        else if (label.text == "Right Arrow")
        {
            uiScript.createArrow("right");
        }
        else if (label.text == "Left Arrow")
        {
            uiScript.createArrow("left");
        }
        else if (label.text == "Down Arrow")
        {
            uiScript.createArrow("down");
        }
        else if (label.text == "Robot")
        {
            uiScript.createObject("robot");
        }
        else if (label.text == "Goal")
        {
            uiScript.createArrow("goal");
        }
        else if (label.text == "Mine")
        {
            uiScript.createArrow("mine");
        }
        else if (label.text == "Wall Horizontal")
        {
            uiScript.createArrow("wall");
        }
        else if (label.text == "Wall Vertical")
        {
            uiScript.createArrow("wall_v");
        }
    }

}
