using System.Collections;
using System.Collections.Generic;
using UnityEngine;

/*
 * Author = Petr Bobčík (xbobci02)
 * 
 * 
 */
public class wallController : MonoBehaviour
{ 

    public GameObject UIManagerObj;
    private UIManager ui_script;
    private bool created_in_editor = false;

    //Can be deleted if created in editor mode
    public void can_be_deleted(bool value)
    {
        this.created_in_editor = true;
    }

    // Start is called before the first frame update
    //Finds UIManager script
    void Start()
    {
        UIManagerObj = GameObject.Find("UIManagerObj");
        ui_script = UIManagerObj.GetComponent<UIManager>();
    }

    void OnMouseDown()
    {
        // Destroy the gameObject after clicking on if delete button was clicked and wall was created in editor
        if (ui_script.deleteMode == true && created_in_editor)
        {
            Destroy(gameObject);
        }
    }
}
