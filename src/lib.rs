// DO NOT modify manually! Generate with `gen_code.py`.
//! Traits to provide a method for dropping values of specific types,
//! as an alternative to a type-agnostic [`drop`] or `_ =` assignment.
//! This is useful to avoid dropping the wrong type, e.g.,
//! when sending a message through a channel.

#[cfg(feature = "tokio")]
use tokio::task::{AbortHandle, JoinHandle};

/// Provides [`DropResult::drop_result`] for dropping [`Result`] values.
pub trait DropResult {
    /// Drop this [`Result`].
    /// This method prevents dropping a value that is not a [`Result`].
    fn drop_result(self);
}

impl<T, E> DropResult for Result<T, E> {
    fn drop_result(self) {}
}

/// Provides [`DropBool::drop_bool`] for dropping [`bool`] values.
pub trait DropBool {
    /// Drop this [`bool`].
    /// This method prevents dropping a value that is not a [`bool`].
    fn drop_bool(self);
}

impl DropBool for bool {
    fn drop_bool(self) {}
}

/// Provides [`DropJoinHandle::drop_join_handle`] for dropping [`JoinHandle`] values.
#[cfg(feature = "tokio")]
pub trait DropJoinHandle {
    /// Drop this [`JoinHandle`].
    /// This method prevents dropping a value that is not a [`JoinHandle`].
    fn drop_join_handle(self);
}

#[cfg(feature = "tokio")]
impl<T> DropJoinHandle for JoinHandle<T> {
    fn drop_join_handle(self) {}
}

/// Provides [`DropAbortHandle::drop_abort_handle`] for dropping [`AbortHandle`] values.
#[cfg(feature = "tokio")]
pub trait DropAbortHandle {
    /// Drop this [`AbortHandle`].
    /// This method prevents dropping a value that is not a [`AbortHandle`].
    fn drop_abort_handle(self);
}

#[cfg(feature = "tokio")]
impl DropAbortHandle for AbortHandle {
    fn drop_abort_handle(self) {}
}
