using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
/*
 * Author = Martin Litwora (xlitwo00)
 * 
 */
public class deathController : MonoBehaviour
{
    public Text death_text; 
    public GameObject UIManagerObj; 
    private UIManager ui_script; 

    // Start is called before the first frame update.
    //Finding UIManager game object, getting its script and getting text component for death_text
    void Start()
    {
        UIManagerObj = GameObject.Find("UIManagerObj");
        ui_script = UIManagerObj.GetComponent<UIManager>();
        death_text = GetComponent<Text>();
    }

    // Update is called once per frame
    //Writing number of deaths on screen 
    void Update()
    {
        death_text.text = " Deaths: \n" + ui_script.number_of_robot_deaths;
    }
}
