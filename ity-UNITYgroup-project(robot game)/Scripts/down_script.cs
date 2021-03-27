using System.Collections;
using System.Collections.Generic;
using UnityEngine;
/*
 * Author = Filip Hruška (xhrusk26)
 * 
 * 
 */
public class down_script : MonoBehaviour
{
    public GameObject UIManagerObj;
    private UIManager ui_script;
    private RobotController robot_script;
 
    //When robot exits this arrow, he changes his movement to go down
    private void OnTriggerExit2D(Collider2D other)
    {
        robot_script = other.GetComponent<RobotController>();
        robot_script.direction = "down";
    }

    void OnMouseDown()
    {
        // Destroy the gameObject after clicking on it\
        if (ui_script.deleteMode == true)
        {
            Destroy(gameObject);
        }
    } 

    //Find UIManager gameobject and get his script
    void Start()
    {
        UIManagerObj = GameObject.Find("UIManagerObj");
        ui_script = UIManagerObj.GetComponent<UIManager>();
    }
}
