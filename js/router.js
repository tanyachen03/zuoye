const Router = {
    routes: {},
    currentRoute: null,
    currentParams: {},

    init() {
        window.addEventListener('hashchange', () => this.handleRoute());
        window.addEventListener('load', () => this.handleRoute());
    },

    register(path, handler) {
        this.routes[path] = handler;
    },

    navigate(path, params = {}) {
        window.location.hash = path;
        this.currentParams = params;
    },

    handleRoute() {
        const hash = window.location.hash.slice(1) || 'home';
        const parts = hash.split('/');
        const route = parts[0];
        const param = parts[1];

        this.currentRoute = route;
        this.currentParams = { id: param };

        if (this.routes[route]) {
            this.routes[route](param);
        } else {
            this.routes['home']();
        }

        this.updateActiveNav();
    },

    updateActiveNav() {
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
            if (link.dataset.page === this.currentRoute) {
                link.classList.add('active');
            }
        });
    },

    getRoute() {
        return this.currentRoute;
    },

    getParam() {
        return this.currentParams.id;
    }
};
