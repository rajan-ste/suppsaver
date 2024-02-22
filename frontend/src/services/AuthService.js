class AuthService {
    login(token) {
        localStorage.setItem('token', token); 
    }

    logout() {
        localStorage.removeItem('token'); 
    }

    getToken() {
        return localStorage.getItem('token'); 
    }

    isAuthenticated() {
        const token = this.getToken();
        return !!token && !this.isTokenExpired(token);
    }

    isTokenExpired(token) {
        try {
            const decoded = JSON.parse(atob(token.split('.')[1]));
            return decoded.exp < Date.now() / 1000;
        } catch (err) {
            return true;
        }
    }
}
export default new AuthService();
