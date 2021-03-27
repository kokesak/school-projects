<!doctype html>
<html lang="en">
<head>
	<meta charset="utf-8" />
	<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
	<meta content='width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0' name='viewport' />
  <meta name="viewport" content="width=device-width" />


  <link href="http://netdna.bootstrapcdn.com/font-awesome/4.4.0/css/font-awesome.css" rel="stylesheet">
  <link href="assets/css/bootstrap.min.css" rel="stylesheet" />
  <link href="assets/css/gsdk-bootstrap-wizard.css" rel="stylesheet" />
  <link rel="stylesheet" href="https://cdn.datatables.net/1.10.20/css/jquery.dataTables.min.css"  type="text/css">
</head>


<body>
<?php
  require "services.php";
  header('Content-type: text/html; charset=utf-8');
  
  $serv = new Service();
  $rows = $serv->getUsers();


?>
  <div class="image-container set-full-height" style="background-image: url('assets/img/main_screen.jpg')">
    <div class="container">
    <div class="alert alert-success collapse" id="deleting_alert">   <!-- collapse hide alert ath the begining -->
            <strong> Deleting information</strong> Are you sure you want to delete this account? <?php echo "AA-$login" ?>
            <input type='button' class='btn-dark btn-fill text-success pull-right' onclick='location.replace("del_user.php?login=<?php echo $login ?>");' name='confirm_delete_acc' value='YES'/>
            <input type='button' class='btn-dark btn-fill text-danger pull-right' onclick="$('#deleting_alert').hide('fade');" name='decline_delete_acc' value='NO'/>
    </div>
      <div class="row">
        <div class="container mb-3 mt-3">
          <table class="table table-striped table-bordered" id="usersTable" style="width:100%">
            <thead>
              <tr>
              <th scope="col">Login</th>
              <th scope="col">Name</th>
              <th scope="col">Surname</th>
              <th scope="col">Position</th>
              </tr>
            </thead>
            <tbody>
            <?php

            while ($row = $rows->fetch())
              {
                  echo "<tr>";
                  echo "<td>" . $row['login'] . "</td>";
                  echo "<td>" . $row['jmeno'] . "</td>";
                  echo "<td>" . $row['prijmeni'] . "</td>";
                  echo "<td>" . $row['typ'] . "</td>";
                  echo '<td class="action">';
                  $login = $row['login'];
                  echo "<a href=\"user_info.php?login=$login\">edit</a> ";
                  echo " | ";
                  echo "<a href='javascript:void(0)' onclick=\"are_you_sure('$login')\">delete</a>";
                  echo "</td>\n";
                  echo "</tr>\n";
              }
            ?>
            </tbody>
          </table>

        </div>

            <div class="wizard-footer height-wizard">
              <input type='button' 
                      class='btn btn-fill btn-warning btn-wd btn-sm pull-left'
                      style="margin:5px;" 
                      onclick="location.replace('index.php');"
                      name='login_btn' 
                      value='Back to menu'/> 
            </div>
    </div>               
  </div>
</div>


	<script src="assets/js/jquery-2.2.4.min.js" type="text/javascript"></script>
	<script src="assets/js/bootstrap.min.js" type="text/javascript"></script>
	<script src="assets/js/jquery.bootstrap.wizard.js" type="text/javascript"></script>
  <script>
        /* When the user clicks on the button, 
        toggle between hiding and showing the dropdown content */
        function are_you_sure(account) {
        //document.write(a);
          if(confirm(`Are you sure you want to delete ${account}?`)){
            location.replace(`del_user.php?login=${account}`);
          }
        }

        function myFunction() {
          document.getElementById("myDropdown").classList.toggle("show");
        }
        
        // Close the dropdown if the user clicks outside of it
        window.onclick = function(event) {
          if (!event.target.matches('.dropbtn')) {
            var dropdowns = document.getElementsByClassName("dropdown-content");
            var i;
            for (i = 0; i < dropdowns.length; i++) {
              var openDropdown = dropdowns[i];
              if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
              }
            }
          }
        }
  </script>


  <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
  <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" type="text/javascript"></script>

  <script src="http://cdn.datatables.net/1.10.19/js/jquery.dataTables.min.js"></script>   <!-- need for searching in table-->
  <script src="http://cdn.datatables.net/1.10.19/js/dataTables.bootstrap4.min.js"></script>
  <script type="text/javascript" src="https://cdn.datatables.net/1.10.20/js/jquery.dataTables.min.js"></script>
  <script text="text/javascript">
      $(document).ready( function () {
          $('#usersTable').DataTable();
      } );
  </script>

</body>
</html>
