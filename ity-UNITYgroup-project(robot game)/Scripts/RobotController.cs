using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

/*
 * Author = Filip Hruška (xhrusk26)
 * 
 * 
 */
public class RobotController : MonoBehaviour
{
    public GameObject UIManagerObj;
    public string direction;
    private UIManager UI_manager;
    public Vector2 origPos;
    Rigidbody2D rigidbody2d;
    private bool created_in_editor = false, is_placed = true;
    public Sprite destroyed_sprite;
    SpriteRenderer renderer;
    public Sprite robot_is_alive_sprite;


    // Start is called before the first frame update
    //Find a UImanager gameobject and get his script
    //Set original position on robot depending where he starts
    //Get his Rigidbody2D, SpriteRenderer and set his default direction value
    void Start()
    {
        UIManagerObj = GameObject.Find("UIManagerObj");
        UI_manager = UIManagerObj.GetComponent<UIManager>();
        origPos = transform.position;
        rigidbody2d = GetComponent<Rigidbody2D>();
        direction = "up";
        renderer = GetComponent<SpriteRenderer>();
    }

    //If he was created in the editor, he can be deleted
    public void can_be_deleted(bool value)
    {
        this.created_in_editor = true;
        this.is_placed = false;
    }

    //If robot was placed, he is influenced by buttons
    public void can_interact()
    {
        this.is_placed = true;
    }

    // Update is called once per frame
    void Update()
    {
        if (is_placed == true)
        {
            //If the robot should move, then he updates his position based on where he should move (position of his rigidbody)
            if (UI_manager.shouldMove == true)
            {
                Vector2 position = rigidbody2d.position;

                if (direction == "up")
                    position.y = position.y + 0.05f;
                else if (direction == "right")
                    position.x = position.x + 0.05f;
                else if (direction == "left")
                    position.x = position.x - 0.05f;
                else if (direction == "down")
                    position.y = position.y - 0.05f;

                rigidbody2d.MovePosition(position);
            }

            //If the robot should reset, he stops moving, goes to his original position, changes his movement direction and changes his sprite (if he was destroyed)
            if (UI_manager.shouldReset == true)
            {
                UI_manager.shouldMove = false;
                transform.position = origPos;
                direction = "up";
                renderer.sprite = robot_is_alive_sprite;
            }
        }
    }

    void OnMouseDown()
    {
        // Destroy the gameObject after clicking on it\
        if (UI_manager.deleteMode == true && created_in_editor)
        {
            Destroy(gameObject);
        }
    }

    //Robot changes his sprite to the destroyed one (when he hits the mine)
    public void explode()
    {
        renderer.sprite = destroyed_sprite;
    }

}
