import { Component, inject } from '@angular/core';
import { SharedService } from '../../services/shared.service';
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  sharedService : SharedService = inject(SharedService);
  router : Router = inject(Router);
  toastr : ToastrService = inject(ToastrService)
  userName: string = '';



  onLogin() {
    if(this.userName) {
      this.sharedService.loggedInInfo(this.userName);
      if (this.userName?.toLowerCase() === 'rohit') {
        this.router.navigate(['/home/upload-csv']);
        this.toastr.success('You\'re now logged in', 'Success...👍', {
          timeOut: 1000,
      });
      } else if(this.userName?.toLowerCase() === 'saqib') {
        this.router.navigate(['/home/employee-overview']);
        this.toastr.success("Login success!");
      }
    }
    else{
      this.toastr.error("Please enter a valid username");
    }
  }

  handleKeyDown(event: KeyboardEvent) {
    if (event.key === 'Enter') {
        event.preventDefault();
        this.onLogin()
        this.userName = '';
    }
  }

}
