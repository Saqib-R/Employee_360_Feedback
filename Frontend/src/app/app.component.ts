import { Component } from '@angular/core';
import { UploadService } from './services/upload.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  ngOnInit(): void {
    window.addEventListener('beforeunload', (event) => {
      localStorage.removeItem('csvData');
      localStorage.removeItem('summary');
      localStorage.removeItem('QueNo');
      localStorage.removeItem('concatenatedResults');
    });
  }

}
