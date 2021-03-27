using System.Collections;
using System.Collections.Generic;
using UnityEngine;

/*
 * Author = Filip Hruška (xhrusk26)
 * 
 * 
 */
public class trashController : MonoBehaviour
{
    private Vector3 mousepos;
    private float dist;

    // Start is called before the first frame update
    //Updates his z value so it is visible to the camera
    void Start()
    {
        dist = transform.position.z - Camera.main.transform.position.z;
    }

    // Update is called once per frame
    //Trash sprite follows mouse on the screen
    void Update()
    {
        mousepos = Camera.main.ScreenToWorldPoint(Input.mousePosition);
        mousepos.z = dist;
        mousepos.x -= 0.15f;
        mousepos.y -= 0.4f;
        transform.position = mousepos;
    }
}
