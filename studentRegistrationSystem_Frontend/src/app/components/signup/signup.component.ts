import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.scss']
})
export class SignupComponent implements OnInit {
  registrationForm!: FormGroup;
  registrationComplete: boolean = false;

  registeredDetails: any = {};

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService
  ) { }

  ngOnInit(): void {
    this.registrationForm = this.formBuilder.group({
      firstname: ['', Validators.required],
      lastname: ['', Validators.required],
      gender: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      age: ['', [Validators.required, Validators.min(18), Validators.max(60)]],
      phonenumber: ['', [Validators.required, Validators.minLength(10), Validators.minLength(10)]],
      password: ['', Validators.required],
      confirmPassword: ['', Validators.required]
    });
  }

  onSubmit() {
    // Validations
    if (this.registrationForm.value.password != this.registrationForm.value.confirmPassword) { this.registrationForm.controls['confirmPassword'].setErrors({ passwordMismatch: true }) }
    if (!this.registrationForm.valid) { this.registrationForm.markAllAsTouched(); }

    this.registrationForm.removeControl('confirmPassword');
    const userDetails = this.registrationForm.value;
    const registerStudentData = {
      "first_name": userDetails.firstname,
      "last_name": userDetails.lastname,
      "age": userDetails.age,
      "gender": userDetails.gender,
      "email": userDetails.email,
      "phone_number": userDetails.phonenumber,
      "password": userDetails.password
    }
    this.authService.register(registerStudentData).subscribe({
      next: (res: any) => {
        this.registrationComplete = true;
        this.registeredDetails = {
          enrollmentId: res.id,
          enrolledFirstname: res.firstname,
          enrolledLastname: res.lastname
        }
      },
      error: (err: any) => {
        alert("Failed to register student. Please try again.")
      }
    });
  }
}
