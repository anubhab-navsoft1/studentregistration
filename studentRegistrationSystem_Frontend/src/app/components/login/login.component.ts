import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  loginForm: FormGroup;
  submitted: boolean = false;

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {
    this.loginForm = this.formBuilder.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required]
    });
  }

  ngOnInit(): void {
    console.log("Value is coming from formBuilder.group",this.loginForm.value);
    console.log("loginForm Controls>>>>>>",this.loginForm.controls['email'])
  }

  onSubmit() {
    this.submitted = true;
    if (this.loginForm.valid) {
      const email = this.loginForm.value.email;
      const password = this.loginForm.value.password;
  
      this.authService.login(email, password).subscribe(
        {
          next: (response) => { // Using 'next' to handle successful response
            console.log('Login successful');
            alert("Login Success");
            this.router.navigate(['/afterlogin']); // Navigate to the dashboard route
          },
          error: (error) => { // Using 'error' to handle errors
            console.log('Login failed:', error);
            alert("Invalid email or password. Please try again.")
            // Handle login error
          }
        }
      );
    } else {
      console.log('Form is invalid');
    }
  }
  
}
