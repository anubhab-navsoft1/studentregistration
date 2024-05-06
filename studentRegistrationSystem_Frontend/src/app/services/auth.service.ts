import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})

export class AuthService {
  private hostUrl = 'http://192.168.3.123:8000';

  constructor(private http: HttpClient) { }

  login(email: string, password: string) {
    return this.http.post<any>(`${this.hostUrl}/studentlogin/`, { email, password });
  }

  register(userDetails: any) {
    return this.http.post<any>(`${this.hostUrl}/studentregister/`, userDetails, {
      headers: { 'Content-Type': 'application/json' }
    });
  }
}
