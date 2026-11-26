import React, { useCallback, useEffect, useRef, useState } from 'react';
import {
  Alert,
  AppBar,
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  Container,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControl,
  FormHelperText,
  InputLabel,
  MenuItem,
  Select,
  Stack,
  TextField,
  Toolbar,
  Typography,
} from '@mui/material';
import ShoppingBagIcon from '@mui/icons-material/ShoppingBag';
import LogoutIcon from '@mui/icons-material/Logout';
import {
  createOrder,
  fetchOrders,
  fetchProducts,
  login,
  type Order,
  type ProductsMap,
} from './api';

export function App() {
  const [token, setToken] = useState<string | null>(null);
  const [currentUser, setCurrentUser] = useState<string>('');

  // Login form state
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loginErrors, setLoginErrors] = useState<{ username?: string; password?: string }>({});
  const [loginLoading, setLoginLoading] = useState(false);
  const [loginServerError, setLoginServerError] = useState<string | null>(null);
  const loginInFlightRef = useRef(false);

  // Shop state
  const [products, setProducts] = useState<ProductsMap>({});
  const [orders, setOrders] = useState<Order[]>([]);
  const [selectedProduct, setSelectedProduct] = useState<string>('');
  const [productError, setProductError] = useState<string | null>(null);

  const [shopLoading, setShopLoading] = useState(false);
  const [shopError, setShopError] = useState<string | null>(null);

  const [orderSubmitting, setOrderSubmitting] = useState(false);
  const [orderSuccess, setOrderSuccess] = useState<string | null>(null);
  const [orderError, setOrderError] = useState<string | null>(null);
  const orderInFlightRef = useRef(false);

  // Order details dialog
  const [activeOrder, setActiveOrder] = useState<Order | null>(null);

  const loadShopData = useCallback(async () => {
    setShopLoading(true);
    setShopError(null);
    try {
      const [prods, ords] = await Promise.all([fetchProducts(), fetchOrders()]);
      setProducts(prods);
      setOrders(ords);
      const keys = Object.keys(prods);
      if (keys.length > 0) {
        setSelectedProduct((prev) => (prev && prods[prev] !== undefined ? prev : keys[0]));
      }
    } catch (err) {
      setShopError(err instanceof Error ? err.message : 'Не удалось загрузить данные магазина');
    } finally {
      setShopLoading(false);
    }
  }, []);

  useEffect(() => {
    if (token) {
      void loadShopData();
    }
  }, [token, loadShopData]);

  const handleLoginSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (loginInFlightRef.current) return;

    const trimmedUser = username.trim();
    const errs: { username?: string; password?: string } = {};
    if (!trimmedUser) {
      errs.username = 'Введите имя пользователя';
    }
    if (!password) {
      errs.password = 'Введите пароль';
    } else if (password.length < 4) {
      errs.password = 'Пароль должен содержать минимум 4 символа';
    }

    if (Object.keys(errs).length > 0) {
      setLoginErrors(errs);
      return;
    }

    setLoginErrors({});
    setLoginServerError(null);
    loginInFlightRef.current = true;
    setLoginLoading(true);

    try {
      const res = await login(trimmedUser, password);
      setToken(res.token);
      setCurrentUser(trimmedUser);
    } catch (err) {
      setLoginServerError(err instanceof Error ? err.message : 'Ошибка авторизации');
    } finally {
      loginInFlightRef.current = false;
      setLoginLoading(false);
    }
  };

  const handleCreateOrder = async (e: React.FormEvent) => {
    e.preventDefault();
    if (orderInFlightRef.current || !token) return;

    if (!selectedProduct) {
      setProductError('Выберите товар из каталога');
      return;
    }

    setProductError(null);
    setOrderError(null);
    setOrderSuccess(null);
    orderInFlightRef.current = true;
    setOrderSubmitting(true);

    try {
      const created = await createOrder(token, selectedProduct);
      setOrders((prev) => [...prev, created]);
      setOrderSuccess(`Заказ #${created.id} (${created.product}) успешно создан!`);
    } catch (err) {
      setOrderError(err instanceof Error ? err.message : 'Не удалось оформить заказ');
    } finally {
      orderInFlightRef.current = false;
      setOrderSubmitting(false);
    }
  };

  const handleLogout = () => {
    setToken(null);
    setCurrentUser('');
    setOrders([]);
    setProducts({});
    setSelectedProduct('');
    setOrderSuccess(null);
    setOrderError(null);
    setShopError(null);
  };

  const productEntries = Object.entries(products);

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'background.default', pb: 6 }}>
      <AppBar position="static" elevation={1}>
        <Toolbar>
          <ShoppingBagIcon sx={{ mr: 1.5 }} aria-hidden="true" />
          <Typography variant="h6" component="h1" sx={{ flexGrow: 1 }}>
            Mini Shop
          </Typography>
          {token && (
            <Stack direction="row" spacing={1.5} alignItems="center">
              <Chip
                label={currentUser}
                color="secondary"
                size="small"
                sx={{ color: '#fff', fontWeight: 600 }}
              />
              <Button
                color="inherit"
                startIcon={<LogoutIcon />}
                onClick={handleLogout}
                size="small"
              >
                Выйти
              </Button>
            </Stack>
          )}
        </Toolbar>
      </AppBar>

      <Container maxWidth="sm" sx={{ mt: 4 }}>
        {!token ? (
          <Card variant="outlined">
            <CardContent sx={{ p: 3 }}>
              <Typography variant="h5" component="h2" gutterBottom>
                Вход в магазин
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2.5 }}>
                Демо-аккаунты: <code>alice</code> / <code>learn-alice</code> или{' '}
                <code>bob</code> / <code>learn-bob</code>
              </Typography>

              {loginServerError && (
                <Alert severity="error" role="alert" sx={{ mb: 2 }}>
                  {loginServerError}
                </Alert>
              )}

              <Box component="form" onSubmit={handleLoginSubmit} noValidate>
                <Stack spacing={2}>
                  <TextField
                    id="username-input"
                    label="Имя пользователя"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    error={Boolean(loginErrors.username)}
                    helperText={loginErrors.username}
                    required
                    fullWidth
                    autoComplete="username"
                  />
                  <TextField
                    id="password-input"
                    label="Пароль"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    error={Boolean(loginErrors.password)}
                    helperText={loginErrors.password}
                    required
                    fullWidth
                    autoComplete="current-password"
                  />
                  <Button
                    type="submit"
                    variant="contained"
                    size="large"
                    disabled={loginLoading}
                    fullWidth
                  >
                    {loginLoading ? (
                      <Stack direction="row" spacing={1} alignItems="center">
                        <CircularProgress size={18} color="inherit" />
                        <span>Вход…</span>
                      </Stack>
                    ) : (
                      'Войти в магазин'
                    )}
                  </Button>
                </Stack>
              </Box>
            </CardContent>
          </Card>
        ) : (
          <Stack spacing={3}>
            <Card variant="outlined">
              <CardContent sx={{ p: 3 }}>
                <Typography variant="h5" component="h2" gutterBottom>
                  Оформить заказ
                </Typography>

                {shopLoading && (
                  <Stack direction="row" spacing={1.5} alignItems="center" sx={{ py: 2 }}>
                    <CircularProgress size={22} aria-label="Загрузка каталога" />
                    <Typography variant="body2" color="text.secondary">
                      Загрузка данных…
                    </Typography>
                  </Stack>
                )}

                {shopError && (
                  <Alert
                    severity="error"
                    role="alert"
                    sx={{ mb: 2 }}
                    action={
                      <Button color="inherit" size="small" onClick={() => void loadShopData()}>
                        Повторить
                      </Button>
                    }
                  >
                    {shopError}
                  </Alert>
                )}

                {orderError && (
                  <Alert severity="error" role="alert" sx={{ mb: 2 }}>
                    {orderError}
                  </Alert>
                )}

                {orderSuccess && (
                  <Alert severity="success" role="status" sx={{ mb: 2 }}>
                    {orderSuccess}
                  </Alert>
                )}

                <Box component="form" onSubmit={handleCreateOrder} noValidate>
                  <Stack spacing={2}>
                    <FormControl fullWidth error={Boolean(productError)}>
                      <InputLabel id="product-select-label">Товар из каталога</InputLabel>
                      <Select
                        labelId="product-select-label"
                        id="product-select"
                        label="Товар из каталога"
                        value={selectedProduct}
                        onChange={(e) => setSelectedProduct(e.target.value)}
                        disabled={shopLoading || productEntries.length === 0}
                      >
                        {productEntries.map(([name, price]) => (
                          <MenuItem key={name} value={name}>
                            {name} — {price} ₽
                          </MenuItem>
                        ))}
                      </Select>
                      {productError && <FormHelperText>{productError}</FormHelperText>}
                    </FormControl>

                    <Button
                      type="submit"
                      variant="contained"
                      size="large"
                      disabled={orderSubmitting || shopLoading}
                      fullWidth
                    >
                      {orderSubmitting ? (
                        <Stack direction="row" spacing={1} alignItems="center">
                          <CircularProgress size={18} color="inherit" />
                          <span>Отправка заказа…</span>
                        </Stack>
                      ) : (
                        'Оформить заказ'
                      )}
                    </Button>
                  </Stack>
                </Box>
              </CardContent>
            </Card>

            <Card variant="outlined">
              <CardContent sx={{ p: 3 }}>
                <Typography variant="h6" component="h2" gutterBottom>
                  Список заказов
                </Typography>

                {!shopLoading && orders.length === 0 ? (
                  <Typography
                    variant="body2"
                    color="text.secondary"
                    sx={{
                      textAlign: 'center',
                      py: 3,
                      border: '1px dashed',
                      borderColor: 'divider',
                      borderRadius: 1,
                    }}
                  >
                    Заказов пока нет
                  </Typography>
                ) : (
                  <Stack spacing={1.5}>
                    {orders.map((order) => (
                      <Box
                        key={order.id}
                        sx={{
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'space-between',
                          gap: 2,
                          p: 1.5,
                          border: '1px solid',
                          borderColor: 'divider',
                          borderRadius: 1,
                        }}
                      >
                        <Box>
                          <Typography variant="subtitle1" component="span" fontWeight={600}>
                            #{order.id} {order.product}
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            {order.price} ₽ · владелец #{order.owner}
                          </Typography>
                        </Box>
                        <Button
                          variant="outlined"
                          size="small"
                          onClick={() => setActiveOrder(order)}
                        >
                          Детали
                        </Button>
                      </Box>
                    ))}
                  </Stack>
                )}
              </CardContent>
            </Card>
          </Stack>
        )}
      </Container>

      <Dialog
        open={Boolean(activeOrder)}
        onClose={() => setActiveOrder(null)}
        aria-labelledby="order-dialog-title"
        fullWidth
        maxWidth="xs"
      >
        <DialogTitle id="order-dialog-title">
          Детали заказа #{activeOrder?.id}
        </DialogTitle>
        <DialogContent dividers>
          {activeOrder && (
            <Stack spacing={1}>
              <Typography variant="body1">
                Товар: <strong>{activeOrder.product}</strong>
              </Typography>
              <Typography variant="body1">
                Стоимость: <strong>{activeOrder.price} ₽</strong>
              </Typography>
              <Typography variant="body2" color="text.secondary">
                ID владельца: {activeOrder.owner}
              </Typography>
            </Stack>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setActiveOrder(null)} autoFocus>
            Закрыть
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default App;
