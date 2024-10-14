import { Component } from '@angular/core';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  userName: string = '';

  onSubmit() {
    if (this.userName) {
      console.log('Name submitted:', this.userName);
      // Handle your logic here, like navigating to another page
    } else {
      alert('Please enter your name');
    }
  }

}
