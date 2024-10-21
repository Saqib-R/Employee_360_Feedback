import { Component, inject } from '@angular/core';
import { SharedService } from '../../services/shared.service';
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css'
})
export class NavbarComponent {
  imgPath : any = './i1.png';
  sharedService : SharedService = inject(SharedService);
  userName : string = '';
  router : Router = inject(Router);
  toastr : ToastrService = inject(ToastrService);


  ngOnInit(): void {
    this.sharedService.loggedIn.subscribe(data => {
      if(data){
        this.userName = data;
      }
    })
  }

  onLogout() {
    this.userName = '';
    localStorage.removeItem('csvData');
    localStorage.removeItem('summary');
    localStorage.removeItem('QueNo');
    localStorage.removeItem('concatenatedResults');
    this.router.navigate(['/login']);
    this.toastr.success("Logout success!")
  }
}
