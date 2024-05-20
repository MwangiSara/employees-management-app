package com.israel.test

import android.os.Bundle
import android.os.Process
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.ProgressBar
import android.widget.TextView
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import org.json.JSONArray
import org.json.JSONObject

class GetEmployee : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_get_employee)
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }// end insets

        val searchForm = findViewById<LinearLayout>(R.id.searchForm)
        searchForm.visibility = View.GONE
        val idNumber = findViewById<EditText>(R.id.id_number)

        val progressbar = findViewById<ProgressBar>(R.id.progressbar)
        val data = findViewById<TextView>(R.id.data)

        val api = "https://manuel09434.pythonanywhere.com/employees"
        //val api ="http://192.168.43.11:5000/employees"


        getEmployees(api = api, textView = data, loader = progressbar, searchForm = searchForm)

        val searchBtn = findViewById<Button>(R.id.searchBtn)
        searchBtn.setOnClickListener{
            if(idNumber.text.toString().isNotEmpty()){
                val newApi = api + "/"+ idNumber.text.toString()
                getSingleEmployee(api = newApi, textView = data, loader = progressbar)
            }else{
                Toast.makeText(applicationContext, "Please enter an ID number ", Toast.LENGTH_SHORT).show()
            }
        }

        val reloadBtn = findViewById<Button>(R.id.reloadBtn)
        reloadBtn.setOnClickListener {
            getEmployees(api = api, textView = data, loader = progressbar, searchForm = searchForm)
        }
    }// end onCreate

    fun getEmployees(api: String, textView: TextView, loader: ProgressBar, searchForm: LinearLayout) {
        textView.text = ""
        loader.visibility =View.VISIBLE
        val apiHelper = ApiHelper(applicationContext)
        apiHelper.get(api, object: ApiHelper.CallBack{
            override fun onSuccess(result: String?) {
                //Create an instance of JSONArray class and pass in the result
                // from the server(This is likely to be an JSONArray of employees)
                val employees = JSONArray(result.toString())

                // Loop through employees JSONArray
                (0 until employees.length()).forEach{
                    // Retrieve each employee in the array using their index
                    var employee = employees.getJSONObject(it)
                    // use append() function to add employee info into TextView
                    textView.append("ID number: ${employee.get("id_number")} \n")
                    textView.append("Username: ${employee.get("username")} \n")
                    textView.append("Salary: ${employee.get("salary")} \n\n")
                }// end forEach
                searchForm.visibility = View.VISIBLE
                loader.visibility = View.GONE
            }// end onSuccess
        })// end get
    }

    fun getSingleEmployee(api: String, textView: TextView, loader: ProgressBar){
        textView.text = ""
        loader.visibility =View.VISIBLE
        val apiHelper = ApiHelper(applicationContext)
        apiHelper.get(api, object: ApiHelper.CallBack{
            override fun onSuccess(result: String?) {
                val employee = JSONObject(result.toString())
                // use append() function to add employee info into TextView
                textView.append("ID number: ${employee.get("id_number")} \n")
                textView.append("Username: ${employee.get("username")} \n")
                textView.append("Salary: ${employee.get("salary")} \n\n")
                loader.visibility = View.GONE
            }// end onSuccess
        })// end get
    }
} // end GeEmployee