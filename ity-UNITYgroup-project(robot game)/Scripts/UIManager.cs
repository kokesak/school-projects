using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;
/*
 * Authors = Petr Bobčík (xbobci02)
 *           Martin Litwora (xlitwo00)
 *           Filip Hruška (xhrusk26)
 */
public class UIManager : MonoBehaviour
{
    public bool shouldMove = false;
    public bool shouldReset = false;
    public bool deleteMode = false;
    public bool startTimer = false;
    private bool newArrowClicked = false, newRoboClicked = false, newWallClicked = false;

    public GameObject up_prefab, down_prefab, left_prefab, right_prefab, parent_grid, trash_prefab, trash_obj, goal_prefab, robot_prefab, mine_prefab, wall_prefab;
    private GameObject newObject;

    private Vector3 localPos;
    BoxCollider2D collider;
    Rigidbody2D roboBody;
    private float dist;
    Grid grid;
    Vector3Int cellPosition;
    RobotController roboScript;
    mineController mine_script;
    goalController goal_script;
    wallController wall_script;
    public GameObject popup, victory_popup;
    float timeLeft = 5.0f;
    public int number_of_robot_deaths = 0;
    private bool bug = true;

    //Changes the game level or scene (xhrusk26)
    public void ChangeScene(string scenename)
    {
        SceneManager.LoadScene(scenename);
    }

    //Starts moving robot and timer (xhrusk26)
    public void startRobot()
    {
        shouldReset = false;
        shouldMove = true;
        startTimer = true;
    }

    //Stops robot and resets him (xhrusk26)
    // If popup is active, turn it off after 5 second (xlitwo00)
    public void resetRobot()
    {
        shouldReset = true;
        if (popup.activeSelf)
        {
            popup.SetActive(false);
            timeLeft = 5.0f;
        }
    }

    //Activate delete mode and create trash next to mouse (xhrusk26)
    public void activateExtermination()
    {
        if (deleteMode != true)
        {
            deleteMode = true;
            trash_obj = Instantiate(trash_prefab, Input.mousePosition, Quaternion.identity);
        }

    }

    //Method for creating robot only, because he is different than other objects (xbobci02)
    public void createObject(string obj)
    {
        if (obj == "robot")
        {
            newObject = Instantiate(robot_prefab, Input.mousePosition, Quaternion.identity, parent_grid.transform); //create robot at mouse position
            roboBody = newObject.GetComponent<Rigidbody2D>(); //Get his rigidbody
            roboBody.isKinematic = true; //Kinematic mode enabled, forces, collisions or joints won't affect the rigidbody (because it is not placed yet)
            roboScript = newObject.GetComponent<RobotController>(); //Get robot script
            roboScript.can_be_deleted(true); //Set that robot can be deleted
        }
        //Sets his position at mouse position and indicate that robot was clicked
        newObject.transform.position = Camera.main.ScreenToWorldPoint(Input.mousePosition);
        dist = newObject.transform.position.z - Camera.main.transform.position.z;
        newRoboClicked = true;
    }

    //Method for creating other objects (xhrusk26, xboci02, xlitwo00)
    public void createArrow(string direction)
    {
        if (direction == "up") //Arrow up (xhrusk26)
            newObject = Instantiate(up_prefab, Input.mousePosition, Quaternion.identity, parent_grid.transform);
        else if (direction == "down") //Arrow down (xhrusk26)
            newObject = Instantiate(down_prefab, Input.mousePosition, Quaternion.identity, parent_grid.transform);
        else if (direction == "left") //Arrow left (xhrusk26)
            newObject = Instantiate(left_prefab, Input.mousePosition, Quaternion.identity, parent_grid.transform);
        else if (direction == "right") //Arrow uright (xhrusk26)
            newObject = Instantiate(right_prefab, Input.mousePosition, Quaternion.identity, parent_grid.transform);
        else if (direction == "goal") //Goal flag (xhrusk26)
        {
            newObject = Instantiate(goal_prefab, Input.mousePosition, Quaternion.identity, parent_grid.transform);
            goal_script = newObject.GetComponent<goalController>();
            goal_script.can_be_deleted(true);
        }

        else if (direction == "wall") //Vertical wall (xbobci02)
        {
            newObject = Instantiate(wall_prefab, Input.mousePosition, Quaternion.identity, parent_grid.transform);
            wall_script = newObject.GetComponent<wallController>();
            wall_script.can_be_deleted(true);
            newWallClicked = true;
        }

        else if (direction == "wall_v") //Horizontal wall(xbobci02)
        {
            newObject = Instantiate(wall_prefab, Input.mousePosition, Quaternion.identity, parent_grid.transform);
            newObject.transform.Rotate(0.0f, 0.0f, 90.0f, Space.Self);
            wall_script = newObject.GetComponent<wallController>();
            wall_script.can_be_deleted(true);
            newWallClicked = true;
        }

        else if (direction == "mine") //Mine (xlitwo00)
        {
            newObject = Instantiate(mine_prefab, Input.mousePosition, Quaternion.identity, parent_grid.transform);
            mine_script = newObject.GetComponent<mineController>();
            mine_script.can_be_deleted(true);
        }


        newObject.transform.localScale += new Vector3(0.1f, 0.1f, 0); //Bigger scale of object (xhrusk26)
        newObject.transform.position = Camera.main.ScreenToWorldPoint(Input.mousePosition); //Object moves to mouse position (xhrusk26)
        collider = newObject.GetComponent<BoxCollider2D>();
        collider.enabled = !collider.enabled; //Disable collider so object can't interact with others, because it's not placed (xbobci02)
        dist = newObject.transform.position.z - Camera.main.transform.position.z;// Set z axis, so camera can see the object (xhrusk26)
        newArrowClicked = true; //Indicates new object is clicked (xhrusk26)
    }

    //Get grid from parent (xhrusk26)
    private void Start()
    {
        grid = parent_grid.GetComponent<Grid>();
    }

    void Update()
    {
        if (newArrowClicked == true || newRoboClicked == true) //if there is any object clicked and ready to be created
        {
            this.startTimer = true; //start timer
            Vector3 mousepos = Camera.main.ScreenToWorldPoint(Input.mousePosition);
            mousepos.z = dist;
            newObject.transform.position = mousepos; //Sets object position to mouse
            if (Input.GetMouseButtonDown(0)) //On mouse left click
            {
                //Find local cell of the grid the object is in and sets localPos to center of that cell (xhrusk26)
                cellPosition = grid.LocalToCell(newObject.transform.localPosition);
                localPos = grid.GetCellCenterLocal(cellPosition);
                if (newWallClicked == true)
                {
                    newObject.transform.position = mousepos; //wall can be placed anywhere and not snapped to center of a cell (xbobci02)
                }
                else
                {
                    newObject.transform.localPosition = localPos; //other objects are snapped to center of a cell (xhrusk26)
                }
                if (newArrowClicked == true || newWallClicked == true)
                    collider.enabled = !collider.enabled; //enable collider, so it can interact with robot (xbobci02)
                else if (newRoboClicked == true)
                {
                    roboBody.isKinematic = false; //turn of kinematic mode for robot (xboci02)
                    roboScript.origPos = newObject.transform.position; //sets robot original position for reset purposes (xboci02)
                    roboScript.can_interact(); //Robot is influenced by buttons (xhrusk26)
                }
                newArrowClicked = false;
                newRoboClicked = false;
                newWallClicked = false;
            }

            //On right click cancel new object being placed (xhrusk26)
            if (Input.GetMouseButtonDown(1))
            {
                Destroy(newObject);
                newArrowClicked = false;
                newRoboClicked = false;
                newWallClicked = false;

            }
        }

        //If delete button was placed, then it can be canceled with right click (xhrusk26)
        if (deleteMode == true)
        {
            if (Input.GetMouseButtonDown(1))
            {
                deleteMode = false;
                Destroy(trash_obj);
            }
        }


        // if any popup is active, then robot should stop moving and popup disappear after some time.. robot is then reseted (xlitwo00)
        if (popup.activeSelf || victory_popup.activeSelf)
        {
            shouldMove = false;
            this.bug = true;
            timeLeft -= Time.deltaTime;
            if (timeLeft < 0)
            {
                popup.SetActive(false);
                victory_popup.SetActive(false);
                timeLeft = 5.0f;
                this.resetRobot();
            }
        }
        
    }

    // shows popup if the robot was destroyed by mine (xlitwo00) 
    public void show_popup(string message)
    {
        popup.GetComponent<Text>().text = message;
        popup.SetActive(true);
        if (this.bug)
        {

            this.bug = false;
            number_of_robot_deaths += 1;
        }
    }

    // shows popup if robot arrived to the goal (xlitwo00)
    public void show_victory_popup(string message)
    {
        victory_popup.GetComponent<Text>().text = message;
        victory_popup.SetActive(true);
        this.startTimer = false;
    }

    //Choose level based on selection from dropdown (xbobci02)
    public void play_mode_dropdown(int value)
    {
        switch (value)
        {
            case 0:
                this.ChangeScene("Play_scene");
                break;
            case 1:
                this.ChangeScene("Play_scene_2");
                break;
            case 2:
                this.ChangeScene("Play_scene_3");
                break; 
        }
    }
}
