import { Component, inject } from '@angular/core';
import { SharedService } from '../../services/shared.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {
  showChatbot = false;

  toggleChatbot() {
    this.showChatbot = !this.showChatbot;
  }

}
