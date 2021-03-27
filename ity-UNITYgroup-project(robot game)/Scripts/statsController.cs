using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
/*
 * Author = Martin Litwora (xlitwo00)
 * 
 * 
 */
public class statsController : MonoBehaviour
{
    public Text timer_text;
    public GameObject UIManagerObj;
    private UIManager ui_script;
    private float minutes, seconds;

    // Start is called before the first frame update
    //Finds UIManager object and get his script
    //Get text for timer
    void Start()
    {
        UIManagerObj = GameObject.Find("UIManagerObj");
        ui_script = UIManagerObj.GetComponent<UIManager>();
        timer_text = GetComponent<Text>();
       // death_text = GetComponent<Text>();
    }

    // Update is called once per frame
    void Update()
    {
        //Counting time
        if (ui_script.startTimer)
        {
            seconds += Time.deltaTime;
            minutes += (int)(seconds / 59f);
            seconds %= 59f;
            timer_text.text = " Time \n" + minutes.ToString("00") + ":" + seconds.ToString("00");
        }
    }
}
