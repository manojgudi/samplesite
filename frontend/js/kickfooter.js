
            var users = [
                {username :"Dravid",userid:1},
                {username :"Sehwag",userid:2},
                {username :"Kohli",userid:3},
                {username :"Dhoni",userid:4},
                {username :"Sachin",userid:5}
            ];
            
            //Initiate Slots and Users
            //Can be linked to database later
            var slots = [
                {
                    displayName: "6AM-7AM",
                    timestamp : (new Date()).setHours(6,0,0,0)
                },
                {
                    displayName: "7AM-8AM",
                    timestamp : (new Date()).setHours(7,0,0,0)
                },
                {
                    displayName: "8AM-9AM",
                    timestamp : (new Date()).setHours(8,0,0,0)
                },
                {
                    displayName: "9AM-10AM",
                    timestamp : (new Date()).setHours(9,0,0,0)
                }
                ,{
                    displayName: "10AM-11AM",
                    timestamp : (new Date()).setHours(10,0,0,0)
                },
                {
                    displayName: "Divider",
                    timestamp : (new Date())
                },{
                    displayName: "6PM-7PM",
                    timestamp : (new Date()).setHours(18,0,0,0)
                },{
                    displayName: "7PM-8PM",
                    timestamp : (new Date()).setHours(19,0,0,0)
                },{
                    displayName: "8PM-9PM",
                    timestamp : (new Date()).setHours(20,0,0,0)
                },{
                    displayName: "9PM-10PM",
                    timestamp : (new Date()).setHours(21,0,0,0)
                }
                ,{
                    displayName: "10PM-11PM",
                    timestamp : (new Date()).setHours(22,0,0,0)
                }
                
            ];
            
            
            //Create HTML checkboxes
            var destinationDiv="#morningSlots";
            for(var i=0; i < slots.length ; i++)
            {
                
                var slotCheckboxHtml="<div class=\"checkbox\">\
                                      <label><input type=\"checkbox\" name=\"slot\" value=\""+slots[i].timestamp+"\">"+slots[i].displayName+"</label>\
                                    </div>";
                if(slots[i].displayName=="Divider")
                {
                    destinationDiv="#eveningSlots"
                    continue;
                }
                $(destinationDiv).append(slotCheckboxHtml);
            }
            
            //Create User dropdown
            for(var i=0; i < users.length ; i++)
            {
                var usersLiHtml="<option value=\""+users[i].userid+"\">"+users[i].username+"</option>";
                $("#users").append(usersLiHtml);
            }
            
            $("#submit").click(function(){
               
               // User Details
               var data_username = $('#users').val();
               var data_userid = 0; // for future use
               data_userid = parseInt(data_userid);
               if(data_username.trim()=="")return false;
               
               // Slot Details
               var data_timestamps=[];    
               var checkboxslots = $("#availabilitySlots input:checkbox");
               for (var i=0;i<checkboxslots.length;i++)
               {
                    if(checkboxslots[i].checked)
                    {
                        data_timestamps.push(parseInt(checkboxslots[i].value));    
                    }
               }
               if(data_timestamps.length == 0) return false;
               
               //Create JSON
               var data_toSend = {
                   username:data_username,
                   userid:data_userid,
                   availability:data_timestamps
               }
               
               $("#output").append("<br/>Posting JSON <br/>");
               $("#output").append(JSON.stringify(data_toSend));
               $("#submit").removeClass("btn-success").addClass("btn-info").addClass("disabled").text("Submitting...");
                $.ajax({
                    url: 'http://52.163.95.79:6767/insertAvailability',
                    type: 'post',
                    dataType: 'json',
                    data: JSON.stringify(data_toSend),
                    success: function (data) {
                        $('#output').append("<br/>Response:<br/>");
                        $('#output').append(JSON.stringify(data));
                        if(data.responseCode==0)
                        {
                            $("#success").show();
                            $("#formContainer").hide();
                        }
                        else{
                            alert("Error"+data.responseStatus);        
                        }
                        
                    },
                    error: function(xhr, textStatus, error){
                          $('#output').append("<br/>Response:<br/>");
                          $('#output').append(xhr.statusText+"<Br/>");
                          $('#output').append(textStatus+"<br/>");
                          $('#output').append(error+"<Br/>");
                      }
                });

            });
            
            
            //Date Formatting
            var monthNames = [
              "January", "February", "March",
              "April", "May", "June", "July",
              "August", "September", "October",
              "November", "December"
            ];

            var date = new Date();
            var day = date.getDate();
            var monthIndex = date.getMonth();
            
            var year = date.getFullYear();
            
            var today = day+  ' ' + monthNames[monthIndex] + ' ' + year;
            
            $(function(){
                $("#today").html(today);
            });