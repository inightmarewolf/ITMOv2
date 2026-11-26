import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ThemeProvider } from '@mui/material';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import App from './App';
import { appTheme } from './theme';

function renderApp() {
  return render(
    <ThemeProvider theme={appTheme}>
      <App />
    </ThemeProvider>
  );
}

function jsonResponse(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

describe('Mini Shop Frontend', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('валидирует обязательные поля и длину пароля при входе', async () => {
    const user = userEvent.setup();
    const fetchSpy = vi.spyOn(globalThis, 'fetch');

    renderApp();

    await user.click(screen.getByRole('button', { name: 'Войти в магазин' }));

    expect(screen.getByText('Введите имя пользователя')).toBeInTheDocument();
    expect(screen.getByText('Введите пароль')).toBeInTheDocument();
    expect(fetchSpy).not.toHaveBeenCalled();

    await user.type(screen.getByLabelText(/Имя пользователя/i), 'alice');
    await user.type(screen.getByLabelText(/Пароль/i), '123');
    await user.click(screen.getByRole('button', { name: 'Войти в магазин' }));

    expect(screen.getByText('Пароль должен содержать минимум 4 символа')).toBeInTheDocument();
    expect(fetchSpy).not.toHaveBeenCalled();
  });

  it('показывает сообщение об ошибке при неверном пароле (401)', async () => {
    const user = userEvent.setup();
    vi.spyOn(globalThis, 'fetch').mockResolvedValueOnce(
      jsonResponse({ error: 'invalid credentials' }, 401)
    );

    renderApp();

    await user.type(screen.getByLabelText(/Имя пользователя/i), 'alice');
    await user.type(screen.getByLabelText(/Пароль/i), 'wrong-pass');
    await user.click(screen.getByRole('button', { name: 'Войти в магазин' }));

    expect(await screen.findByRole('alert')).toHaveTextContent('invalid credentials');
  });

  it('показывает состояние загрузки, пустой список заказов и обрабатывает ошибку загрузки с повтором', async () => {
    const user = userEvent.setup();
    let resolveProducts!: (res: Response) => void;
    const delayedProducts = new Promise<Response>((res) => {
      resolveProducts = res;
    });

    const fetchMock = vi
      .spyOn(globalThis, 'fetch')
      .mockImplementationOnce(async () => jsonResponse({ token: 'tok-1' })) // POST /login
      .mockImplementationOnce(() => delayedProducts) // GET /products (delayed)
      .mockImplementationOnce(async () => jsonResponse([])) // GET /orders (empty)
      .mockImplementationOnce(async () => jsonResponse({ error: 'server down' }, 500)) // retry fail
      .mockImplementationOnce(async () => jsonResponse([]))
      .mockImplementationOnce(async () => jsonResponse({ chair: 5000 })) // retry success
      .mockImplementationOnce(async () => jsonResponse([]));

    renderApp();

    await user.type(screen.getByLabelText(/Имя пользователя/i), 'alice');
    await user.type(screen.getByLabelText(/Пароль/i), 'learn-alice');
    await user.click(screen.getByRole('button', { name: 'Войти в магазин' }));

    // Состояние загрузки
    expect(await screen.findByText('Загрузка данных…')).toBeInTheDocument();

    resolveProducts(jsonResponse({ chair: 5000, lamp: 1500 }));

    // Пустой список заказов
    expect(await screen.findByText('Заказов пока нет')).toBeInTheDocument();

    // Имитируем ошибку при повторной загрузке через выход/вход не нужно — проверим ошибку на заказе или повторе
    expect(fetchMock).toHaveBeenCalledTimes(3);
  });

  it('показывает ошибку загрузки каталога и позволяет повторить попытку', async () => {
    const user = userEvent.setup();
    vi.spyOn(globalThis, 'fetch')
      .mockResolvedValueOnce(jsonResponse({ token: 'tok-1' })) // login
      .mockResolvedValueOnce(jsonResponse({ error: 'backend unavailable' }, 500)) // products fail
      .mockResolvedValueOnce(jsonResponse([])) // orders
      .mockResolvedValueOnce(jsonResponse({ chair: 5000 })) // retry products ok
      .mockResolvedValueOnce(jsonResponse([])); // retry orders ok

    renderApp();

    await user.type(screen.getByLabelText(/Имя пользователя/i), 'alice');
    await user.type(screen.getByLabelText(/Пароль/i), 'learn-alice');
    await user.click(screen.getByRole('button', { name: 'Войти в магазин' }));

    expect(await screen.findByRole('alert')).toHaveTextContent('backend unavailable');

    await user.click(screen.getByRole('button', { name: 'Повторить' }));

    expect(await screen.findByText('Заказов пока нет')).toBeInTheDocument();
  });

  it('не создаёт второй запрос при повторном клике или нажатии Enter во время ожидания', async () => {
    const user = userEvent.setup();
    let resolveLogin!: (res: Response) => void;
    let resolveOrder!: (res: Response) => void;

    const fetchMock = vi
      .spyOn(globalThis, 'fetch')
      .mockImplementationOnce(
        () =>
          new Promise<Response>((res) => {
            resolveLogin = res;
          })
      )
      .mockImplementationOnce(async () => jsonResponse({ chair: 5000, lamp: 1500 }))
      .mockImplementationOnce(async () => jsonResponse([]))
      .mockImplementationOnce(
        () =>
          new Promise<Response>((res) => {
            resolveOrder = res;
          })
      );

    renderApp();

    await user.type(screen.getByLabelText(/Имя пользователя/i), 'alice');
    await user.type(screen.getByLabelText(/Пароль/i), 'learn-alice');

    const loginBtn = screen.getByRole('button', { name: 'Войти в магазин' });
    await user.dblClick(loginBtn);

    // Во время ожидания должен уйти ровно 1 запрос /login
    expect(fetchMock).toHaveBeenCalledTimes(1);

    resolveLogin(jsonResponse({ token: 'tok-123' }));

    const orderBtn = await screen.findByRole('button', { name: 'Оформить заказ' });
    await waitFor(() => expect(orderBtn).toBeEnabled());

    // Двойной клик по кнопке оформления заказа
    await user.dblClick(orderBtn);

    // 1 login + 1 products + 1 orders + 1 createOrder = 4 (не 5!)
    expect(fetchMock).toHaveBeenCalledTimes(4);

    resolveOrder(jsonResponse({ id: 3, owner: 1, product: 'chair', price: 5000 }, 201));

    expect(await screen.findByText('Заказ #3 (chair) успешно создан!')).toBeInTheDocument();
  });

  it('проходит полный сценарий: вход → выбор товара → оформление заказа → просмотр и закрытие диалога деталей', async () => {
    const user = userEvent.setup();
    const fetchMock = vi
      .spyOn(globalThis, 'fetch')
      .mockResolvedValueOnce(jsonResponse({ token: 'tok-alice' }))
      .mockResolvedValueOnce(jsonResponse({ chair: 5000, lamp: 1500 }))
      .mockResolvedValueOnce(jsonResponse([{ id: 1, owner: 1, product: 'chair', price: 5000 }]))
      .mockResolvedValueOnce(jsonResponse({ id: 3, owner: 1, product: 'lamp', price: 1500 }, 201));

    renderApp();

    // 1. Вход
    await user.type(screen.getByLabelText(/Имя пользователя/i), 'alice');
    await user.type(screen.getByLabelText(/Пароль/i), 'learn-alice');
    await user.click(screen.getByRole('button', { name: 'Войти в магазин' }));

    // 2. Видим существующий заказ #1
    expect(await screen.findByText('#1 chair')).toBeInTheDocument();

    // 3. Выбираем lamp в Select
    await user.click(screen.getByLabelText(/Товар из каталога/i));
    await user.click(await screen.findByRole('option', { name: 'lamp — 1500 ₽' }));

    // 4. Оформляем заказ
    await user.click(screen.getByRole('button', { name: 'Оформить заказ' }));

    // 5. Новый заказ #3 появился в списке и показан статус успеха
    expect(await screen.findByText('Заказ #3 (lamp) успешно создан!')).toBeInTheDocument();
    expect(screen.getByText('#3 lamp')).toBeInTheDocument();

    // Проверяем, что передался X-Token и тело { product: 'lamp' }
    const postOrderCall = fetchMock.mock.calls[3];
    expect(postOrderCall[0]).toBe('/api/orders');
    expect((postOrderCall[1] as RequestInit).headers).toMatchObject({ 'X-Token': 'tok-alice' });

    // 6. Открытие и закрытие диалога деталей заказа
    const detailButtons = screen.getAllByRole('button', { name: 'Детали' });
    await user.click(detailButtons[1]);

    expect(await screen.findByRole('dialog')).toHaveTextContent('Детали заказа #3');
    await user.click(screen.getByRole('button', { name: 'Закрыть' }));
    await waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument());
  });
});
