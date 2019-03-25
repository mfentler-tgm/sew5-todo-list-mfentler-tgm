<template>
  <div>
  <h1>Todo-Liste</h1>
    <h2>Add Task</h2>
    <table align="center">
        <tr>
          <td><input v-model="task_name" placeholder="Task-Name"></td>
          <td><input v-model="task_description" placeholder="Task-Description"></td>
          <td><input type="button" value="Add" v-on:click="postUser()"/></td>
        </tr>
    </table>
    <hr>
    <form ref="editTaskForm" hidden="true" v-on:submit="putUser()">
      <h2>Edit Task</h2>
      <table align="center">
         <tr>
           <td><input v-model="editform.task_name"></td>
          <td><input v-model="editform.task_description"></td>
          <td><input type="submit" value="Update" /></td>
         </tr>
      </table>
      <hr>
    </form>
    <table align="center">
      <thead>
        <tr>
          <td>Name</td>
          <td>Description</td>
          <td>&nbsp;</td>
          <td>&nbsp;</td>
        </tr>
      </thead>
      <tbody>
        <tr v-for="task in tasks">
            <td><input :value="task.name" disabled></td>
            <td><input :value="task.description" disabled></td>
            <td><input type="button" value="Edit" v-on:click="putUserPreparation(task.id,task.name,task.description)" /></td>
            <td><input type="button" value="Delete" v-on:click="deleteUser(task.id)"/></td>
        </tr>
      </tbody>
    </table>

  </div>
</template>

<script>
  import axios from 'axios'

  export default {
  name: "Task",
  data() {
    return{
      tasks: [],
      task_name: "",
      task_description: "",
      editform: {
        id: "",
        task_name: "",
        task_description: ""
      }
    }
  },
  methods: {
    getUser() {
      const path = 'http://localhost:5000/'
      axios({
          method:'get',
          url: path,
          auth:{
            username: 'admin',
            password: '1234'
          }
        })
        .then((res) => {
          this.tasks = res.data
        })
        .catch((error) => {
        // eslint-disable-next-line
          console.error(error)
        })
    },
    deleteUser(id){
      const path = 'http://localhost:5000/' + id
      axios({
          method:'delete',
          url: path,
          auth:{
            username: 'admin',
            password: '1234'
          }
        })
        .then((res) => {
          this.getUser()
        })
        .catch((error) => {
          console.error(error)
        })
    },
    postUser() {
      const path = 'http://localhost:5000/'
      if(this.task_name == "" || this.task_description == ""){
        console.error("Give all arguments")
        return
      }
      axios({
          method:'post',
          url: path,
          auth:{
            username: 'admin',
            password: '1234'
          },
          data:{
            name:this.task_name,
            description:this.task_description
          }
        })
        .then((res) => {
          this.getUser()
          this.initFields()
        })
        .catch((error) => {
        // eslint-disable-next-line
          console.error(error)
          alert("Task name has to be unique")
        })
    },
    putUserPreparation(id, name, des){
      this.editform.id = id
      this.editform.task_name = name
      this.editform.task_description = des
      this.$refs.editTaskForm.hidden = false
    },
    putUser(){
      const path = 'http://localhost:5000/' + this.editform.id
      if (this.editform.task_name == '' || this.editform.task_description == ''){
        alert("Parameter is not allowed to be ' '")
        return
      }
      axios({
          method:'put',
          url: path,
          auth:{
            username: 'admin',
            password: '1234'
          },
          data:{
            name: this.editform.task_name,
            description: this.editform.task_description
          }
        })
        .then((res) => {
          this.getUser()
          this.initFields()
        })
        .catch((error) => {
          console.error(error)
          alert("Task name has to be unique")
        })

    },
    initFields(){
      this.task_name = "",
      this.task_description = ""
      this.editform.task_name = ""
      this.editform.task_description = ""
      this.editform.id = ""
      this.$refs.editTaskForm.hidden = true
    }
  },
  mounted () {
      this.getUser()
    }
  }
</script>

<style scoped>

</style>
