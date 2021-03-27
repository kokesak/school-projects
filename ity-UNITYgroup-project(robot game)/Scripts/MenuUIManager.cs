using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

/*
 * Author = Filip Hruška (xhrusk26)
 */
public class MenuUIManager : MonoBehaviour
{

    //Changes the game level or scene (xhrusk26)
    public void ChangeScene(string scenename)
    {
        SceneManager.LoadScene(scenename);
    }
    //Quits game (xhrusk26)
    public void ExitGame()
    {
        Application.Quit();
    }
}
