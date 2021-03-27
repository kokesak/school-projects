using System.Collections;
using System.Collections.Generic;
using UnityEngine;

/*
 * Authors = Martin Litwora (xlitwo00), Filip Hruška (xhrusk26)
 * 
 */
public class goalController : MonoBehaviour
{
    public GameObject victoryCanvas, mainCanvas, UIManager, next_level_btn;
    private UIManager UI_script;
    private bool created_in_editor = false;

    public void Start()
    {
        UIManager = GameObject.Find("UIManagerObj");
        mainCanvas = GameObject.Find("Canvas");
        UI_script = UIManager.GetComponent<UIManager>();
    }

    //After entering goal, stop robot and show victory popup
    private void OnTriggerEnter2D(Collider2D collision)
    {
        UI_script.shouldMove = false;
        UI_script.show_victory_popup("You won");
    }

    void OnMouseDown()
    {
        // Destroy the gameObject after clicking on it\
        if (UI_script.deleteMode == true && created_in_editor)
        {
            Destroy(gameObject);
        }
    }

    //If the goal was created in editor, it can be deleted
    public void can_be_deleted(bool value)
    {
        this.created_in_editor = true;
    }

}
