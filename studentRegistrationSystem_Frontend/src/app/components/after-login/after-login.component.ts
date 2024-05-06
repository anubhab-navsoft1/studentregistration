import { Component } from '@angular/core';
import { Router } from '@angular/router';
@Component({
  selector: 'app-after-login',
  templateUrl: './after-login.component.html',
  styleUrl: './after-login.component.scss'
})
export class AfterLoginComponent {
  constructor(private router: Router) { }
  logout() {
    // Perform any logout actions here (e.g., clearing local storage, etc.)
    // Then, navigate to the login page
    this.router.navigate(['/login']);
  }
}
