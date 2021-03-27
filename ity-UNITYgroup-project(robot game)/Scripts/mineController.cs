using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
/*
 * Author = Martin Litwora (xlitwo00)
 * 
 */
public class mineController : MonoBehaviour
{

    public GameObject UIManagerObj;
    private UIManager ui_script;
    private bool created_in_editor = false;
    private RobotController robot_script;

    //When robot touches the mine, he stops moving, explodes and popup is shown
    private void OnTriggerEnter2D(Collider2D collision)
    {
        robot_script = collision.GetComponent<RobotController>();
        robot_script.explode();
        ui_script.shouldMove = false;

        ui_script.show_popup("Robot was destroyed by mine!");
    }

    //If the mine was created in editor, it can be deleted
    public void can_be_deleted(bool value)
    {
        this.created_in_editor = true;
    }

    // Start is called before the first frame update
    //Find UIManager object and take his script
    void Start()
    {
        UIManagerObj = GameObject.Find("UIManagerObj");
        ui_script = UIManagerObj.GetComponent<UIManager>();
    }


    void OnMouseDown()
    {
        // Destroy the gameObject after clicking on it\
        if (ui_script.deleteMode == true && created_in_editor)
        {
            Destroy(gameObject);
        }
    }
}
